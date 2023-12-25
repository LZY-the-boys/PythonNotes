from typing import Optional, List

import torch.distributed as dist
from torch.utils.data import Sampler

import numpy as np
import numba


# @numba.njit
def ffd_check(a: np.ndarray, c: int, n: int):
    # 检查n个gpu(每个gpu有c长度容量)是否足够塞下a(长度)数组
    # First-fit-decreasing bin packing: Check if a could fit in n bins with capacity c
    # n bin = n gpu; c capacity = c seqlen
    # 不等价于 a fit in 1 bins with capacity n*c 
    # 因为每个箱子的任务大小都不能超过其容量c。如果一个任务大小超过单个箱子的容量c，但是没有超过n*c，虽然总的资源是够的，但由于不能跨箱子执行任务，所以这个任务还是不能进行
    # https://en.wikipedia.org/wiki/First-fit-decreasing_bin_packing

    a = np.sort(a)[::-1]
    bins = np.full((n, ), c, dtype=a.dtype)
    # 贪心的看a里边的每个元素是否能够放进某个箱子
    for size in a:
        not_found = True
        for idx in range(n):
            if bins[idx] >= size:
                bins[idx] -= size
                not_found = False
                break

        if not_found:
            return False

    return True


# @numba.njit
def ffd_with_result(a: np.ndarray, c: int, start_index: int):
    # 相比ffd_check，额外记录每个任务分配至哪一个gpu中
    # First-fit-decreasing bin packing (with result return)

    # len max to len min
    indices = np.argsort(a)[::-1]
    a = a[indices]

    bins = []
    bins_result = []
    for a_id, size in enumerate(a):
        add_new = True
        for idx in range(len(bins)):
            if bins[idx] >= size:
                bins[idx] -= size
                bins_result[idx].append(indices[a_id] + start_index)
                add_new = False
                break

        if add_new:
            bins.append(c - size)
            bins_result.append([indices[a_id] + start_index])

    # [
    #     gpu0: 79, 98, 41, 90, ..
    #     gpu1: 55, 105, 106, 107, ..
    #     ..
    #     gpu7: 116, 32, 140
    # ]
    return bins_result


# @numba.njit
def allocate(lengths: np.ndarray, lengths_cumsum: np.ndarray, rank: int, c: int, n: int):
    # Dynamic batch allocator, similar to Multifit
    # https://en.wikipedia.org/wiki/Multifit_algorithm
    # ~99.5% efficiency on OpenChat training set (12 * 2048 ctx len)

    # c: batch * ctx-len 对于同rank上一次forward吃的数据量
    # n: word-size
    # c*n: total seqlen for one forward
    s = 0
    start_index = 0
    result = []

    while True:
        # binary search [l, r)
        # 这个方法按照任务大小的递减顺序对任务进行排序，所以实际上长的任务应该是被先跑的
        # 用二分查找法来找到可以装入当前batch的最大任务集合[start_index:start_index + l]
        # 比如： 见readme.md
        # 1. [0, 159]
        # 2. [159, 167]
        # 3. ...
        l = 1
        # s + c * n 意为当前forward后可分配的长度总量
        # 在 lengths_cumsum[start_index:]数组中查找第一个大于 s + c * n的元素位置
        # 在剩余的任务序列中寻找第一个使总任务量超过计划分配量的任务的位置
        r = 1 + np.searchsorted(lengths_cumsum[start_index:], s + c * n, "right")

        while r - l > 1:
            m = (l + r) // 2
            if ffd_check(lengths[start_index:start_index + m], c, n):
                l = m
            else:
                r = m

        # use length l
        # 计算l下的gpu任务分配
        batch = ffd_with_result(lengths[start_index:start_index + l], c, start_index)
        assert len(batch) <= n
        print(start_index,start_index + l, lengths_cumsum[start_index + l - 1])
        if len(batch) < n:
            break
        
        start_index += l
        s = lengths_cumsum[start_index - 1]

        # add local rank
        result.append(batch[rank])

    # batches, 
    # s=total_used 最后一批样本的累计token？其实应该少算了一个， 应该是lengths_cumsum[start_index + l - 1]
    # len(lengths) 是data item数目，理论forward数目是 len(lengths)/(n*batch)
    # len(result) 是实际的forward数目
    # total_slots 是实际训练使用的总seqlen
    return result, s, len(result) * c * n


class MultipackDistributedBatchSampler(Sampler):
    """Unpadded length sampling using Multipack.
       Approximate (at most ~1.22x) the optimal solution of the identical-machines scheduling problem, which is NP-hard."""
    def __init__(
        self,
        batch_max_length: int,
        lengths: List[int],
        num_replicas: Optional[int] = None,
        rank: Optional[int] = None,
        seed: int = 0,
    ):
        # Get rank
        if num_replicas is None:
            if not dist.is_available():
                raise RuntimeError("Requires distributed package to be available")
            num_replicas = dist.get_world_size()
        if rank is None:
            if not dist.is_available():
                raise RuntimeError("Requires distributed package to be available")
            rank = dist.get_rank()

        self.num_replicas = num_replicas
        self.rank = rank
        self.seed = seed

        self.batch_max_length = batch_max_length
        self.lengths = lengths
        assert isinstance(self.lengths, np.ndarray)

        self.epoch = 0

        # statistics
        self.eff_total_used = 0
        self.eff_total_slots = 0

    def set_epoch(self, epoch: int):
        self.epoch = epoch

    def generate_batches(self, set_stats=False):
        # permuted ids
        indices = np.random.default_rng(seed=self.seed + self.epoch).permutation(len(self.lengths))
        # array([1871, 2048,  881, ..., 2048, 2048, 2048])
        lengths = self.lengths[indices]
        # array([   1871,    3919,    4800, ..., 9517204, 9519252, 9521300])
        lengths_cumsum = np.cumsum(lengths)
        # batches (selected ids for permuted ids): [98, 87, 44, 90, 91, 92, 93, 41, 39, 96, 97, 100, 86, 38, 102, 37]
        # total_used 9402390 数据的总seqlen
        # total_slots 9437184 实际训练使用的总seqlen
        # total_used / total_slots = packing效率
        batches, total_used, total_slots = allocate(
            lengths=lengths,
            lengths_cumsum=lengths_cumsum,
            rank=self.rank,
            c=self.batch_max_length,
            n=self.num_replicas
        )
        batches = [indices[batch] for batch in batches]

        # statistics
        if set_stats:
            self.eff_total_used += total_used
            self.eff_total_slots += total_slots

        return batches

    def __iter__(self):
        batches = self.generate_batches(set_stats=True)
        return iter(batches)

    def num_batches(self):
        batches = self.generate_batches()
        return len(batches)

    def efficiency(self):
        return self.eff_total_used / self.eff_total_slots


if __name__ == "__main__":
    import json
    DATASET = "testdata.json"
    BATCH_SIZE = 16
    CTX_LEN = 2048
    NUM_GPUS = 8
    EPOCHS = 10

    SAMPLERS = {
        "Multipack": lambda lengths, rank: MultipackDistributedBatchSampler(
            lengths=lengths, batch_max_length=BATCH_SIZE * CTX_LEN, num_replicas=NUM_GPUS, rank=rank
        ),
    }

    # Load testdata lengths
    with open(DATASET, "r") as f:
        lengths = np.array(json.load(f))

    # test sampler correctness & efficiency
    for sampler_name, sampler_fn in SAMPLERS.items():
        print(f"Sampler {sampler_name}:")

        tot_len = 0
        tot_batches = 0

        samplers = [sampler_fn(lengths=lengths, rank=rank) for rank in range(NUM_GPUS)]
        print([sampler.num_batches() for sampler in samplers])

        for epoch in range(EPOCHS):
            batches = []
            tot_length = [[] for _ in range(NUM_GPUS)]

            for rank, sampler in enumerate(samplers):
                sampler.set_epoch(epoch)
                for batch in sampler:
                    batches.extend(batch)

                    # Check constraints
                    overall_len = sum([lengths[x] for x in batch])
                    assert overall_len <= BATCH_SIZE * CTX_LEN

                    # Add stats
                    tot_len += overall_len
                    tot_batches += 1

            # Check overall unique
            batches.sort()
            assert batches == list(set(batches))  # Unique

        # Check efficiency
        print(f"Overall Efficiency: {tot_len / (tot_batches * CTX_LEN * BATCH_SIZE)}")
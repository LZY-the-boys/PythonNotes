### Ray

> vllm 使用ray OpenAI应该也是[ray](https://github.com/ray-project/ray)； Python类似的框架有[Dask](https://github.com/dask/dask) 和另外一个就是 [flink](https://github.com/apache/flink)
> https://www.zhihu.com/question/355506071/answer/902074667

启动ray的程序叫`Driver Process`, 被启动的分布式程序成为`Worker/Actor`

- 注册任务：`@ray.remote`

```
@ray.remote
def f(x):
    return x * x
```

- 非阻塞执行普通函数，并行执行 `futures=f.remote(args)`  
- 执行类的方法，同一个类的执行串行，不同类并行 `actor = Class.remote(args)` `futures = actor.method.remote(args)`  

![img](https://pic3.zhimg.com/v2-01eb40db2ce79bd607378a10057a82ba_r.jpg)

- `objects = ray.get(futures)`阻塞执行,  返回真实值
- `ready_futures = ray.wait(futures, k, timeout)`当futures中有k个future完成时，或执行时间超过timeout时，返回futures中已经执行完的future

![img](https://pic2.zhimg.com/v2-dda04ba8e907cb0790d707012acd2911_r.jpg)

![img](https://pic1.zhimg.com/v2-cbe42bc877209b3abbfd2e8fa8a11d50_r.jpg)

GCS 储存了代码、输入参数、返回值。
Worker 通过 Local Scheduler 来和 GCS 通信。
Local Scheduler 就是 Raylet， 是单机上的基础调度服务

- https://zhuanlan.zhihu.com/p/460600694
- https://zhuanlan.zhihu.com/p/111340572
- paper: https://arxiv.org/abs/1712.05889
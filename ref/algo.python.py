from typing import Any, Dict, List, Optional, Tuple, Union, overload
from collections import OrderedDict

class Trie:
    """
    Trie in Python. Creates a Trie out of a list of words. The trie is used to split on `added_tokens` in one pass
    Loose reference https://en.wikipedia.org/wiki/Trie
    """

    def __init__(self):
        self.data = {}

    def add(self, word: str):
        """
        Passes over every char (utf-8 char) on word and recursively adds it to the internal `data` trie representation.
        The special key `""` is used to represent termination.

        This function is idempotent, adding twice the same word will leave the trie unchanged

        Example::

            >>> trie = Trie()
            >>> trie.add("Hello 友達")
            >>> trie.data
            {"H": {"e": {"l": {"l": {"o": {" ": {"友": {"達": {"": 1}}}}}}}}}
            >>> trie.add("Hello")
            >>> trie.data
            {"H": {"e": {"l": {"l": {"o": {"": 1, " ": {"友": {"達": {"": 1}}}}}}}}}
        """
        if not word:
            # Prevent empty string
            return
        ref = self.data
        for char in word:
            ref[char] = char in ref and ref[char] or {}
            # a and b => 只要a!=None 返回后面一个值b; a or b 返回a,如果a==None返回b
            # 在里边: ref[char]
            # 不在里边: {}
            # ref=None: {} (为了防止ref不存在所以要ref and ref[char] 如果ref=None短路特性就不会访问ref[data])
            ref = ref[char]
        ref[""] = 1

    def split(self, text: str) -> List[str]:
        """
        Will look for the words added to the trie within `text`. Output is the original string splitted along the
        boundaries of the words found.

        This trie will match the longest possible word first !

        Example::

            >>> trie = Trie()
            >>> trie.split("[CLS] This is a extra_id_100")
            ["[CLS] This is a extra_id_100"]
            >>> trie.add("[CLS]")
            >>> trie.add("extra_id_1")
            >>> trie.add("extra_id_100")
            >>> trie.split("[CLS] This is a extra_id_100")
            ["[CLS]", " This is a ", "extra_id_100"]
        """
        # indexes are counted left of the chars index.
        # "hello", index 0, is left of h, index 1 is between h and e.
        # index 5 is right of the "o".

        # States are going to capture every possible start (indexes as above)
        # as keys, and have as values, a pointer to the position in the trie
        # where we're at. This is a partial match for now.
        # This enables to keep track of multiple matches while we're iterating
        # the string
        # If the trie contains, "blowing", and "lower" and we encounter the
        # string "blower", we need to split into ["b", "lower"].
        # This is where we need to keep track of multiple possible starts.
        states = OrderedDict()

        # This will contain every indices where we need
        # to cut.
        # We force to cut at offset 0 and len(text) (added later)
        offsets = [0]

        # This is used by the lookahead which needs to skip over
        # some text where the full match exceeded the place in the initial
        # for loop
        skip = None
        # Main loop, Giving this algorithm O(n) complexity
        for current, current_char in enumerate(text):
            if skip and current < skip:
                # Prevents the lookahead for matching twice
                # like extra_id_100 and id_100
                continue

            # This will track every state
            # that stop matching, we need to stop tracking them.
            # If we look at "lowball", we're going to match "l" (add it to states), "o", "w", then
            # fail on "b", we need to remove 0 from the valid states.
            to_remove = set()
            # Whenever we found a match, we need to drop everything
            # this is a greedy algorithm, it will match on the first found token
            reset = False

            # In this case, we already have partial matches (But unfinished)
            for start, trie_pointer in states.items():
                if "" in trie_pointer:
                    # This is a final match, we need to reset and
                    # store the results in `offsets`.

                    # Lookahead to match longest first
                    # Important in case of extra_id_1 vs extra_id_100
                    lookahead_index = current
                    end = current
                    next_char = text[lookahead_index] if lookahead_index < len(text) else None
                    while next_char in trie_pointer:
                        trie_pointer = trie_pointer[next_char]
                        lookahead_index += 1
                        if "" in trie_pointer:
                            end = lookahead_index
                            skip = lookahead_index

                        if lookahead_index == len(text):
                            # End of string
                            break
                        next_char = text[lookahead_index]
                    # End lookahead

                    # Storing and resetting
                    offsets.append(start)
                    offsets.append(end)
                    reset = True
                elif current_char in trie_pointer:
                    # The current character being looked at has a match within the trie
                    # update the pointer (it will be stored back into states later).
                    trie_pointer = trie_pointer[current_char]

                    # Storing back the new pointer into the states.
                    # Partial matches got longer by one.
                    states[start] = trie_pointer
                else:
                    # The new character has not match in the trie, we need
                    # to stop keeping track of this partial match.
                    # We can't do it directly within the loop because of how
                    # python iteration works
                    to_remove.add(start)

            # Either clearing the full start (we found a real match)
            # Or clearing only the partial matches that didn't work.
            if reset:
                states = {}
            else:
                for start in to_remove:
                    del states[start]

            # If this character is a starting character within the trie
            # start keeping track of this partial match.
            if current_char in self.data:
                states[current] = self.data[current_char]

        # We have a cut at the end with states.
        for start, trie_pointer in states.items():
            if "" in trie_pointer:
                # This is a final match, we need to reset and
                # store the results in `offsets`.
                end = len(text)
                offsets.append(start)
                offsets.append(end)
                # Longest cut is always the one with lower start so the first
                # item so we need to break.
                break

        # We have all the offsets now, we just need to do the actual splitting.
        # We need to eventually add the first part of the string and the eventual
        # last part.
        offsets.append(len(text))
        tokens = []
        start = 0
        for end in offsets:
            if start == end:
                # This might happen if there's a match at index 0
                # we're also preventing zero-width cuts in case of two
                # consecutive matches
                continue
            tokens.append(text[start:end])
            start = end

        return tokens

    def main(self):
        trie = Trie()
        trie.add("Hello 友達")
        trie.add("Hello")
        trie.split("[CLS] Hello 友達my friend")


class Solution(object):
    def twoSum(self, nums, target):
        """
        在nums中 找出 和为目标值 target的那 两个 整数，并返回它们的数组下标。
        :type nums: List[int]  [2,7,11,15]
        :type target: int 26
        :rtype: List[int]  [2,3]
        """
        dic = {}
        for i,l in enumerate(nums):
            if target-l in dic:
                return dic[target-l],i
            dic[l]=i
        return None

# 翻转字符串的0-i 
# 时间复杂度 O(n) 因为字符串不可变 所以空间复杂度O(n)
class Solution(object):
    def reversePrefix(self, word, ch):
        i = word.find(ch)+1 # 注意+1 因为翻转的部分包含ch
        return ''.join(reversed(word[:i]))+word[i:] # 不用''.join 报错reversed类型不是str
        # string[start:stop:step]
        return word[:i][::-1] + word[i:]
        return word[i::-1]+word[i]

    def sortEvenOdd(self, nums: List[int]) -> List[int]:
        nums[::2] = sorted(nums[::2])
        nums[1::2] = sorted(nums[1::2], reverse=True) # 非递增
        return nums

class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode  [9,9,9,9,9,9,9]
        :type l2: ListNode  [9,9,9,9]
        :rtype: ListNode [8,9,9,9,0,0,0,1]
        """
        dummy = ListNode(0,None)
        head = dummy
        c = 0
        while l1 and l2:
            head.next = ListNode((l1.val+l2.val+c)%10,None)
            c = (l1.val+l2.val+c)/10
            head = head.next
            l1 = l1.next
            l2 = l2.next
        while l1:
            head.next = ListNode((l1.val+c)%10,None)
            c = (l1.val+c)/10
            head = head.next
            l1 = l1.next
        while l2:
            head.next = ListNode((l2.val+c)%10,None)
            c = (l2.val+c)/10
            head = head.next
            l2 = l2.next
        if c:
            head.next = ListNode(c,None)
            head = head.next
        return dummy.next

    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        re = ListNode(0)
        r = re
        carry=0
        while(l1 or l2):
            x= l1.val if l1 else 0
            y= l2.val if l2 else 0
            s=carry+x+y
            carry=s//10
            r.next=ListNode(s%10)
            r=r.next
            if l1:l1=l1.next
            if l2:l2=l2.next
        if carry:
            r.next=ListNode(carry) # 1
        return re.next



class Solution(object):
    """
    1725 https://leetcode-cn.com/problems/number-of-rectangles-that-can-form-the-largest-square/
    """
    def countGoodRectangles(self, rectangles):
        """
        :type rectangles: List[List[int]]
        :rtype: int
        """
        am,cnt = 0,0
        for x,y in rectangles:
            am = max(min(x,y),am)
        for x,y in rectangles:
            if min(x,y)==am:
                cnt+=1
        return cnt

    def countGoodRectangles(self, rectangles):
        """
        :type rectangles: List[List[int]]
        :rtype: int
        """
        max_len,cnt = 0,0
        for width, height in rectangles:
            cur_len = min(width, height)
            if cur_len > max_len:
                max_len = cur_len
                cnt = 1
            elif cur_len == max_len:
                cnt += 1
        return cnt

class Solution:
    def findMinFibonacciNumbers(self, k:int) -> int :
        """
        返回和为 k 的斐波那契数字(Fi)的最少数目 每个斐波那契数字都可以被使用多次。
        k: int <=1e9
        """

        def calcFibonacciNumbers():
            fibonacciList = [1,1]
            i,lastest=0,1
            while lastest <= k :
                lastest = fibonacciList[i+1]+fibonacciList[i]
                fibonacciList.append(lastest)
                i+=1
            return fibonacciList

        list = calcFibonacciNumbers()
        # 典型的背包问题 复杂度O(len*n)=1e9! 
        d = [k+1]*(k+1)
        d[1] = 1
        for num in range(2,k+1):
            for l in list:
                if l > num: 
                    continue
                elif l==num:
                    d[num] = 1
                else:
                    d[num]=min(d[num],d[num-l]+1)
        return d[k]
    
    def findMinFibonacciNumbers(self, k):
        """
        返回和为 k 的斐波那契数字(Fi)的最少数目 每个斐波那契数字都可以被使用多次。
        :type k: int 9083494
        :rtype: int
        """

        def calcFibonacciNumbers():
            fibonacciList = [1,1]
            while fibonacciList[-1] <= k :
                fibonacciList.append(fibonacciList[-1]+fibonacciList[-2]) # 妙用
            return fibonacciList

        list = calcFibonacciNumbers()
        # 贪心想法: 每次选取最接近k的数字 O(lgk) 因为所有不超过k的斐波那契数字就是lgk个
        # 证明：
        # 注意第一步中f[-1]肯定满足<=k 肯定不需要二分
        i ,cnt = -1, 0
        while k:
            if k>= list[i]:
                k -= list[i]
                cnt += 1
            i -=1
        return cnt

    def findMinFibonacciNumbers(self, k):
        # 空间O(1)优化：不需要求list
        a,b = 1,1
        while b<=k:
            a,b = b,a+b
        i ,cnt = -1, 0
        while k:
            if k>= b:
                k -= b
                cnt += 1
            a,b = b-a,a
        return cnt

class Solution:
    def getMaximumGold(self, grid: List[List[int]]) -> int:
        """
        采矿规则：
        每当矿工进入一个单元，就会收集该单元格中的所有黄金。
        矿工每次可以从当前位置向上下左右四个方向走。
        每个单元格只能被开采（进入）一次。
        不得开采（进入）黄金数目为 0 的单元格。
        矿工可以从网格中 任意一个 有黄金的单元格出发或者是停止。
        最多 25 个单元格中有黄金
        """
        m,n,ans = len(grid),len(grid[0]),0
        def dfs(gold,x,y):
            rec = grid[x][y]
            gold = gold+grid[x][y]
            nonlocal ans # only works in python3
            ans = max(gold,ans)
            grid[x][y] = 0 #vis

            for d in [1,0],[-1,0],[0,1],[0,-1]:
                nx,ny = x+d[0],y+d[1]
                if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] > 0:
                    dfs(gold,nx,ny)
            
            grid[x][y] = rec
        
        for x in range(m):
            for y in range(n):
                if grid[x][y]:
                    dfs(0,x,y)
        
        return ans

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    # 中序遍历： 左 根 右
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        list = []
        
        def dfs(root: Optional[TreeNode]):
            if root==None:
                return 
            if root.left: 
                dfs(root.left)
            list.append(root.val)
            if root.right: 
                dfs(root.right)

        dfs(root)
        return list

    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        result = []
        stack = []
        while stack or root:
            if root:
                stack.append(root)
                root = root.left
            else:
                root = stack.pop()
                result.append(root.val)
                root = root.right
        return result

class SolutionL6019(object):
    def replaceNonCoprimes(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        def gcd(a,b):
            return gcd(b,a%b) if b!=0 else a
        
        def lcm(a,b):
            return a*b/gcd(a,b)

        st = [nums[0]]
        for num in nums[1:]:
            st.append(num)
            while len(st) > 1:
                # if gcd(nums[-1],nums[-2])==1: ...
                if gcd(st[-1],st[-2])==1:
                    break
                st[-2] = lcm(st[-1],st[-2])
                st.pop()    # st[:-1] del(st[-1])        
        return st

class SolutionL6016:
    def cellsInRange(self, s: str) -> List[str]:
        l = []
        for i in range(ord(s[0]),ord(s[3])+1): # ord: char -> int 不能用int('a')
            for j in range(ord(s[1]),ord(s[4])+1): # 可以用int('0') 相应的下面应该是str(j)
                l.append(chr(i)+chr(j)) # chr: int -> char
        # [chr(i)+chr(j) for i in range(ord(s[0]),ord(s[3])+1) for j in range(int(s[1]),int(s[4])+1)]
        return l

class SolutionL6017:
    def minimalKSum(self, nums: List[int], k: int) -> int:
        upper = k
        minus = 0
        last = None
        nums.sort()  
        # 关于list的去重和排序：
        # 不是nums = nums.sort()! return None
        # set(nums) hash无序
        # dict和OrderedDict.fromkeys(nums) 必须是动态插入才是有序的，直接初始化是无序的
        # Python3.6 改写了 dict 的内部算法，Python3.6 版本以后的 dict 是有序的
        for num in nums:
            if num <= upper and num!=last:
                upper+=1
                minus+=num
                last = num
        return int(upper*(upper+1)/2 - minus)

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class SolutionL6018:
    def createBinaryTree(self, descriptions: List[List[int]]) -> Optional[TreeNode]:
        lookuptable = defaultdict(TreeNode)        
        """
        如果试着自己对第一个值做初始化操作，这就会变得很杂乱。例如，可能会写下这样的代码：
        d = {}
        for key, value in pairs:
            if key not in d:
                d[key] = []
            d[key].append(value)
        如果使用defaultdict的话，代码会简单一些：
        d = defaultdict(list)
        for key, value in pairs:
            d[key].append(value)
        """
        hasp = set()
        for p,c,l in descriptions:
            if(l):
                lookuptable[p].left = lookuptable[c]
            else:
                lookuptable[p].right = lookuptable[c]
            hasp.add(c)
        root = None
        for v, i in lookuptable.items():
            i.val = v
            if v not in hasp:
                root = i
        # return [i for v, i in lookuptable.items() if v not in hasp][0]
        # return next(i for v, i in lookuptable.items() if v not in hasp) generator
        return root


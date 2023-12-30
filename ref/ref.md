### 赋值 拷贝 操作

`b = a` 赋值: 只是复制了新对象的引用，不会开辟新的内存空间
`b = a[1:2] = copy.copy(a)` 浅拷贝: 创建新对象，其内容是原对象的引用。
`b= copy.deepcopy(a)` 深拷贝：完全创建一个新的对象

不可变对象拷贝（字符串、元组、数值类型）时和“赋值”的情况一样
当浅复制的值是可变对象（列表、字典、集合）时，复制的对象中有复杂子对象（例如列表中的一个子元素是一个列表）如果不改变其中复杂子对象，浅复制的值改变并不会影响原来的值。 但是改变原来的值中的复杂子对象的值会影响浅复制的值。
```

```

C中变量可以理解成内存位置，Python不是，都是reference。Python的所有变量都是对象的引用，这也包括基本类型。
![Integer Memory Layout](https://jakevdp.github.io/PythonDataScienceHandbook/figures/cint_vs_pyint.png)

- “可变对象” (mutable) 指的是对象自身的“内容”可以被修改，而不是对象指向能否修改 (是否通过赋值操作让变量指向新的对象 (这个是永远可以的) )。
- Python 传参既不是传值 也不是传指针
- 定义默认参数要牢记一点：默认参数必须指向不变对象！

基础类型如int，str等在Python中是不可变的
tuple不可变，即里边的每个元素指向永远不变。即指向`'a'`，就不能改成指向`'b'`，但指向的`a`本身是可变/不可变都行的！
```
a = 5 # 当你声明 a = 5，这就是创建了一个整数对象5，并将该对象的引用（地址）赋值给变量a
a = 6 # 在内存中，你其实创建了一个新的整数对象6，并将其引用赋给了a，而之前的整数对象5并没有被改变。

t = ([1, 2, 3],)
t[0] = [1] # 不合法
t[0].append(4) # 允许

```

list, dict: 可变对象
dict的key必须是**不可变对象** hash （str是不变对象，而list是可变对象）

```
aa = []
bb = []
aa.append(bb)
bb.append(1)
aa => [[1]]

# 处理数据的时候的常见坑点
b = []
while True:
    a = [xx] # a指向别的位置，原位置数据没变
    b.append(a) # b指向位置不变，该位置数据变化，
    data = [a,b] # a不会变 b会
    data = [a,copy.deepcopy(b)] # 正确做法
```

在PyTorch中，torch.Tensor对象是可变的。
这种可变性使得在进行操作时我们能够直接更新或修改张量的值，而不是创建新的张量。
例如，可以通过索引(param[0], param[:], param.data)直接修改张量中的元素，或者使用一些in-place方法来直接更新张量的值，这些方法的名字通常以_结尾，例如add_()，mul_()等。

```
param = tensor_A # A的引用
param = torch.Tensor([1, 2, 3]) # A未变，param引用对象变
param[:] = torch.Tensor([1, 2, 3]) # 原址（原来的张量对象）上直接修改了它的值，所以A会改变

# 这里是实现上的逻辑决定的
param.add(tensor_A) # 返回一个新tensor
param.add_(tensor_A) # in place

for module in model.modules():
    # 合法的，内部实现
    module.to(torch.bfloat16)

for param in model.parameters():
    # param是引用，而非副本
    # 直接修改param 那么它将变为一个新的对象，因为param (torch.Tensor)是不可变的引用 直接将param设置为新的张量，其实是创建了一个新的张量，并把param指向它，但原模型参数还是指向原来的张量
    # 如果你想更改模型参数的值，你需要对其具体的元素进行操作，例如param.data.add_(1)或者param[0] = 100, 这种方式能行是因为 param是引用

    # 错误写法
    param = param.to(torch.bfloat16)
    # 这里要用 module.data 才能真正修改原值
    param.data = param.data.to(torch.bfloat16)
```

### 垃圾回收

Python中，主要通过引用计数（Reference Counting）进行垃圾回收。
```
typedef struct_object {
 int ob_refcnt;
 struct_typeobject *ob_type;
} PyObject;
```

https://zhuanlan.zhihu.com/p/108683483 

- 程序在运行的过程中会实时的更新ob_refcnt的值，来反映引用当前对象的名称数量。当某对象的引用计数值为0,那么它的内存就会被立即释放掉。
- Python采用了“标记-清除”(Mark and Sweep)算法，解决容器对象可能产生的循环引用问题。
- Python 通过“分代回收”(Generational Collection)以空间换时间的方法提高垃圾回收效率

https://www.zhihu.com/question/20053359 python 为什么不支持重载


### 内存泄露

https://zhuanlan.zhihu.com/p/338232671

```
import numpy as np
n = 50
l = []
for i in range(n):
    array_large = np.random.choice(1000, size=(7000, 7000))
    array_small = array_large[:5, :5]
    array_small = array_large[:5, :5].copy()
    l.append(array_small)
``` 
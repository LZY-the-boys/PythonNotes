#### 基本语法：

分支循环

```python
if age >= 18:
    print('adult')
elif age >= 6:
    print('teenager')
else:
    print('kid')
```

```python
while n > 0:
    sum = sum + n
    n = n - 2
#for x in 可迭代对象:
for i in [0, 10]:
    sum = sum + x
```



###### `*` 和`**`

- function definition
  - The `*args` will give you all function parameters as **tuple**
  - The `**kwargs` will give you all **keyword arguments** except for those corresponding to a formal parameter as a **dictionary**.

```python
def foo(*args):
    for a in args:
        print(a)        

foo(1)
# 1

foo(1,2,3)
# 1
# 2
# 3

# matrix = [[1, 2, 3, 4],[5, 6, 7, 8],[9, 10, 11, 12],]
list(zip(*matrix)) # [(1, 5, 9), (2, 6, 10), (3, 7, 11), (4, 8, 12)]
```

```python
def bar(**kwargs):
    for a in kwargs:
        print(a, kwargs[a])  

bar(name='one', age=27)
# name one
# age 27
```

- function call
  - `*l` unpack argument list
  - `**d` unpack argument dictionary

```python
def foo(a, b, c):
    print(a, b, c)

obj = {'b':10, 'c':'lee'}
foo(100,**obj)
# 100 10 lee
l=[1,2,3]
foo(*l)
# 1 2 3
```



#### [Data structures](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)

###### List

> 在CPython中，列表被实现为长度可变的数组(vector) 而非链表
>  `collections`模块提供了名为`Deque`的双端队列

```python
for i, l in enumerate(list):
    print(i, l)
for item in zip([1, 2, 3], [4, 5, 6]):
    print(item) # (1, 4) (2,5) ...
first, second, *reset = 0, 1, 2, 3 # reset = [2,3]
```

List 实现queue是低效的，因为pop/append需要$O(n)$的移动

```python
# stack
stack.append(7)
stack.pop()
# queue
from collections import deque
queue = deque(["Eric", "John", "Michael"])
queue.append("Terry") 
queue.popleft()  
```

List comprehensions [列表推导]

```python
squares = list(map(lambda x: x**2, range(10)))
squares = [x**2 for x in range(10)]
[(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]
#>>> combs = []
#>>> for x in [1,2,3]:
#...     for y in [3,1,4]:
#...         if x != y:
#...             combs.append((x, y))
[(x, x**2) for x in range(6)] # 不加括号会报错
# vec = [[1,2,3], [4,5,6], [7,8,9]] flatten 2D
[num for elem in vec for num in elem]
[[row[i] for row in matrix] for i in range(4)] # [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]

```

用法

```python
list = [0]*10
list2 = [0 for i in range(10)]

a = [list()] * 5 # 浅拷贝
a[0].append(1) # [[1], [1], [1], [1], [1]] 
a = [list() for i in range(5)]
a[0].append(1) # [[1], [], [], [], []]
```

numpy `[:,1] ` https://docs.scipy.org/doc/numpy-1.10.1/reference/arrays.indexing.html#basic-slicing-and-indexing

###### Dictionaries

> CPython使用伪随机探测(pseudo-random probing)的散列表(hash table)作为字典的底层数据结构,所以内部键的顺序是无序的 key必须是**不可变对象** hash （str是不变对象，而list是可变对象）
>  `collections`模块提供了名为`OrderedDict`的有序字典

```python
>>> tel = {'jack': 4098, 'sape': 4139} 
>>> dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
>>> dict(sape=4139, guido=4127, jack=4098) # only when keys are simple string
>>> {x: x**2 for x in (2, 4, 6)}

>>> tel['guido'] = 4127 # insert
>>> del tel['sape']
>>> list(tel) # key: ['jack', 'guido', 'irv']
>>> sorted(tel) # ['guido', 'irv', 'jack']
>>> 'guido' in tel # check
>>> 'jack' not in tel

for k, v in tel.items():
...     print(k, v)
```

###### Set

> 集合被实现为带有空值的字典，只有键才是实际的集合元素



#### 参数传递

首先一点，C中变量可以理解成内存位置，Python不是，都是reference。

Python中一切皆对象，对象分为两种类型，可变对象`mutable`和不可变对象`immutable`，不可变对象指tuple、str、int等类型的对象，可变对象指的是dict、list、自定义class等类型的对象

Python 传参既不是传值 也不是传指针

```python
# id(obj)得到obj的内存地址(10进制)
a = [1, 2, 3]
print(id(a))  # 2038473041600
a += [4]
print(id(a))  # 2038473041600

def fun1(arg):
    print(id(arg)) # 2038473041600
    arg += [4]
    print(id(arg)) # 2038473041600

fun1(a)


b = 1
print(id(b))  # 140710214770432
b += 1
print(id(b))  # 140710214770464

def fun2(arg):
    print(id(arg)) # 140710214770464
    arg += 1
    print(id(arg))  # 140710214770496

fun2(b)
```

```python
import copy

a = 1  # id: 140710211297024
b = a  # id: 140710211297024
a = 2  # id: 140710211297056
print(b)  # 1

a = [1, 2, 3]  # id: 2149596997696
b = a  # id: 2149596997696
a.append(4)
print(a, b)  # [1, 2, 3, 4] [1, 2, 3, 4]

a = [1, 2, 3]  # id: 2149596997312
b = copy.copy(a)  # id: 2149537582016
a.append(4)
print(a, b) # [1, 2, 3, 4] [1, 2, 3]

# 当列表或字典参数里面的值是列表或字典时，copy并不会复制参数里面的列表或字典
a=[1,[1,2],3]
b=copy.deepcopy(a)
a[1].append(4)

# list 和 dict都是可变对象
ref = {'h':{'e': {'l': {'l': {'o': {' ': {'友': {'達': {'': 1}}}}}}}}}
for char in 'hello':
    ref[char] = char in ref and ref[char] or {} # ref[char] or {}
    ref = ref[char] # 就和指针一样

head = ListNode(0,None)
while l1 and l2:
	head.next = ListNode((l1.val+l2.val),None)
	head = head.next # 并不会改变前面组好的linklist 对于c/cpp必须是指针类型才有这个效果
```



#### Class

>  数据封装、继承和多态是面向对象的三大特点

```python
class A(): # A 继承B
    x = '0' # 类变量
    def __init__(self,x,y): # constructor
        self.x = x # 实例变量
        self.y = y

    def method_a(self, foo): # self = this
        print self.x + ' ' + foo
        
a = A('1','2') # call __init__ method, x='1',y='2'
a.method_a('3') # call method_a, don't need self, foo = '3'
```

注意一点：`self` 未必叫self，可以是其它名字，规定instance methods的第一个参数叫self，class methods的第一个参数叫cls

```python
class RetroReader:
	def __init__(self,xx):
	
	@classmethod
	def load(cls,xx):
		return cls(xx) # 构造该类 并调用__init__()
```



- 私有变量：`__`开头 一般不可在类外访问

```python
class Student(object):

    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_score(self):
        print('%s: %s' % (self.__name, self.__score))
        
bart = Student('Bart Simpson', 59)
bart.__name # 无法访问
bart._Student__name # 后门：不能直接访问__name是因为Python解释器对外把__name变量改成了_Student__name，所以，仍然可以通过_Student__name来访问__name变量：
bart.__name = 'New Name' # 这里实际是新增加了一个变量__name
```

- 特殊变量：`__xxx__` 

  - `__slots__`变量，限制该class实例能添加的属性

    子类也定义slots后，子类实例允许定义的属性才是自身的`__slots__`加上父类的`__slots__`

  ```python
  class Student(object):
      __slots__ = ('name', 'age') # 用tuple定义允许绑定的属性名称
  ```

- 特殊方法：`__len__()`  

  - `len(A)`会自动调用A的`__len__() `  ，自己的类实现了`__len__()`后也可以调用`len()`

    > 用`len(xxx)`和`xxx.__len__()`是一样的

  - `A[5]`: 调用`__getitem__()` 

    > torch.util.dataset 只需要`__len__()`和`__getitem__()`两个方法即可定义

  - `print(A)`会调用A的`__str__()`

  - `A`  在console里直接显示变量调用的是`__repr__()` 一般可以直接`__repr__ = __str__`

  - `for .. in A`: 调用`__iter__()`和iter返回对象的`__next__()`

    ```python
    next(dict.__iter__())
    ```

  - 调用不存在的属性`__getattr__()` 可以用作防御，也可以把一个类的所有属性和方法调用全部动态化处理了，比如REST API，根据url实现动态的调用

  - 定义一个`__call__()`方法，就可以直接对实例进行调用，这时完全可以把对象看成函数，把函数看成对象

    > model(data)之所以等价于model.forward(data)，就是因为在类（class）中使用了`__call__`函数
    
    the `__init__` method is used when the *class* is called to initialize the instance, while the `__call__` method is called when the *instance* is called
    
    ```python
    class Foo:
        def __init__(self, a, b, c):
            # ...
        def __call__(self, a, b, c):
            # ...
    
    x = Foo(1, 2, 3) # __init__
    
    x = Foo()
    x(1, 2, 3) # __call__
    ```
    
  
- 三种方法: 静态方法(staticmethod),类方法(classmethod)和实例方法

  ```python
  class A(object):
      def foo(self,x): # 实例方法 和self绑定 a.foo(x)(其实是foo(a, x)).
          print "executing foo(%s,%s)"%(self,x)
  
      @classmethod
      def class_foo(cls,x): # 类方法 和类绑定 A.class_foo(x)/a.class_foo(x)
          print "executing class_foo(%s,%s)"%(cls,x)
  
      @staticmethod
      def static_foo(x): # 静态方法 不绑定 但是通过a.static_foo(x)/A.static_foo(x)来调用.
          print "executing static_foo(%s)"%x
  ```

- 类变量和实例变量

  ```python
  class A(B): 
      x = '0' # 类变量
      z = '1'
      def __init__(self,x=0,y=0): 
          self.x = x # 实例变量
          self.y = y
  
  a = A(1,0)
  b = A()
  a.x # '1'
  A.x # '0'
  a.z = '2' # 修改的是实例变量
  b.z # '1'
  del a.x;a.x # '0' 相同名称的实例属性将屏蔽掉类属性，但是当你删除实例属性后，再使用相同的名称，访问到的将是类属性。
  ```

- [==继承==]：对于静态语言（例如Java）来说，如果需要传入`Animal`类型，则传入的对象必须是`Animal`类型或者它的子类，否则，将无法调用`run()`方法。对于Python这样的动态语言来说，则不一定需要传入`Animal`类型。我们只需要保证传入的对象有一个`run()`方法就可以了：（动态语言的“鸭子类型”）

  ```python
  class A(B):
  	pass # A 继承B
  class Dog(Mammal, Runnable):
      pass # 多重继承
  ```

- [自省]运行时获取对象类型

  - type方法
  
  ```python
  type(xxx) # <class '...'>
  if type(fn)==types.FunctionType # 函数类型
  ```
  
  - isinstance方法
  
  ```python
  isinstance(h, Animal)
  ```
  
  - dir方法： 获得一个对象的所有属性和方法
  
  ```python
  dir('ABC') # ['__add__', '__class__',..., '__subclasshook__',   'capitalize', 'casefold',..., 'zfill']
  ```
  
  - attr方法
  
  ```python
  hasattr(obj, 'x') # 有属性'x'吗？
  setattr(obj, 'y', 19) # 设置一个属性'y'
  getattr(obj, 'y') # 获取属性'y'
  # 对于一个未知文件流，首先要判断是否有read方法
  def readImage(fp):
      if hasattr(fp, 'read'):
          return readData(fp)
      return None
  ```

  > 在Python这类动态语言中，根据鸭子类型，有`read()`方法，不代表该fp对象就是一个文件流，它也可能是网络流，也可能是内存中的一个字节流，但只要`read()`方法返回的是有效的图像数据，就不影响读取图像的功能。

  - 需要判断一个对象是否能被调用(是否实现了`__call__()`)，能被调用的对象就是一个`Callable`对象

  ```python
  callable(max) # True
  callable([1, 2, 3]) # False
  ```

- 没有函数重载！
  - python已经支持：函数功能相同，参数类型不同
  - 缺省参数可以实现：函数功能相同，但参数个数不同

枚举

```python
from enum import Enum
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')) #默认从1开始计数。
```

自定义方式

```python
from enum import Enum, unique
@unique #@unique装饰器可以帮助我们检查保证没有重复值。
class Weekday(Enum):
    Sun = 0 # Sun的value被设定为0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
```



[meta-class](https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python)

只要有 `class`, Python executes it and creates an **object**.  it's an object, and therefore:

- you can assign it to a variable
- you can copy it
- you can add attributes to it
- you can pass it as a function parameter

```python
>>> class ObjectCreator(object):       
		pass
# creates in memory an object with the name `ObjectCreator`. 
>>> print(MyClass) # the function returns a class, not an instance
<class '__main__.Foo'>
>>> print(MyClass()) #  (the class) is itself capable of creating objects (the instances)
<__main__.Foo object at 0x89c6d4c>
```

现在需要动态创建class 可以用`type(,,)`：

```python
# type(name, bases, attrs) bases=tuple of the parent class attrs=dicts of attributes
>>> MyShinyClass = type('MyShinyClass', (), {}) # returns a class object
>>> print(MyShinyClass)
<class '__main__.MyShinyClass'>
>>> print(MyShinyClass()) # create an instance with the class
<__main__.MyShinyClass object at 0x8997cec>

# add method to class
>>> def echo_bar(self):
...       print(self.bar)
...
>>> FooChild = type('FooChild', (Foo,), {'echo_bar': echo_bar})
```

这是因为 `type` is in fact a metaclass!!!

`Metaclass` are the 'stuff' that creates classes. They are the classes' classes, you can picture them this way:

```py
MyClass = MetaClass()
my_object = MyClass()
```

The main purpose of a metaclass is to change the class automatically, when it's created.The main use case for a metaclass is creating an API. A typical example of this is the `Django ORM`. It allows you to define something like this:

https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python



#### 文件IO操作

[Fastest way to process a large file?](https://stackoverflow.com/questions/30294146/fastest-way-to-process-a-large-file)

您的代码是受 I/O 限制还是受 CPU 限制？换句话说，处理是否比读取花费更多时间？如果是这样，您可能可以通过多处理来加速它；如果没有，您的后台进程将把所有时间都花在等待下一次读取上，而您将得不到任何好处

`for line in infile:`已经在`io`模块代码中实现了缓冲，但你想强制它使用更大的缓冲区，可以`infile.readlines(65536)`然后循环每个块中的行

Each line has 54 characters in seven fields . remove the last three characters from each of the first three fields (60GBfile)

```python
# 70700.642014 31207.277115 -0.054123 -1585 255 255 255
def ProcessLargeTextFile():
    with open("filepath", "r") as r, open("outfilepath", "w") as w:
        for line in r:
            x, y, z = line.split(' ')[:3]
            w.write(line.replace(x,x[:-3]).replace(y,y[:-3]).replace(z,z[:-3]))
            # or
            x, y, z, rest = line.split(' ', 3)
            bunch.append(' '.join((x[:-3], y[:-3], z[:-3], rest)))
# 考虑一次一个块
def ProcessLargeTextFile():
    bunchsize = 1000000     # Experiment with different sizes
    bunch = []
    with open("filepath", "r") as r, open("outfilepath", "w") as w:
        for line in r:
           	x, y, z = line.split(' ')[:3]
           bunch.append(line.replace(x,x[:-3]).replace(y,y[:-3]).replace(z,z[:-3]))
            if len(bunch) == bunchsize:
                w.writelines(bunch)
                bunch = []
        w.writelines(bunch)
```

counting line-num ：

```python
num_lines = sum(1 for line in open('myfile.txt'))
```

[Find duplicate records in large text file]

```python
# To speed up access you could use the first e.g. 2 bytes of the hash as the key of a collections.defaultdict and put the rest of the hashes in a list in the value.
d = collections.defaultdict(list)
with open('bigdata.txt', 'r') as datafile:
    for line in datafile:
        id = hashlib.sha256(line).digest()
        # Or id = line[:n]
        k = id[0:2]
        v = id[2:]
        if v in d[k]:
            print "double found:", id
        else:
            d[k].append(v)
```

 check whether a file exists without exceptions

```python
import os.path
os.path.isfile(fname) 

from pathlib import Path
    my_file = Path("/path/to/file")
    if my_file.is_file():
        
	if my_file.is_dir():
    
    if my_file.exists():
     
try:
    my_abs_path = my_file.resolve(strict=True)
except FileNotFoundError:
    # doesn't exist
else:
    # exists
```



```python
import os
for s_child in os.listdir(s_path):
    s_child_path = os.path.join(s_path, s_child)
    if os.path.isdir(s_child_path):
    else:
```



#### TODO

###### 默认参数

定义默认参数要牢记一点：默认参数必须指向不变对象！

###### 闭包

返回函数不要引用任何循环变量，或者后续会发生变化的变量
内部函数不能改变外部函数中变量的指向

```python
# can use to read code and run in pycharm but cannot run in cmd
from src.models.CCIG.util.nlp_utils import split_sentence
from src.models.CCIG.util.list_utils import common, substract, remove_values_from_list

#  can use to read code in pycharm but cannot run both in cmd and pycharm
from ..util.nlp_utils import split_sentence
from ..util.list_utils import common, substract, remove_values_from_list

# commandline can use :
from util.nlp_utils import split_sentence
from util.list_utils import common, substract, remove_values_from_list
```



```python
x = np.random.rand(3,2)
>> array([[ 0.03196827,  0.50048646],
       [ 0.85928802,  0.50081615],
       [ 0.11140678,  0.88828011]])

x = x[:,1]
>> array([ 0.50048646,  0.50081615,  0.88828011])
```

列表生成 

```python
[x * x for x in range(1, 11) if x % 2 == 0] #不加else
[m + n for m in 'ABC' for n in 'XYZ']
tokens = [token for line in tokens for token in line]
[k + '=' + v for k, v in d.items()]
[x if x % 2 == 0 else -x for x in range(1, 11)]
```

##### generator： 

列表元素可以按照某种算法推算出来，那我们是否可以在循环的过程中不断推算出后续的元素呢？这样就不必创建完整的list，从而节省大量的空间

```python
g = (x * x for x in range(10)) # [] -> ()
next(g) #可能StopIteration错误
for x in g:
```

```python
def fib(max):
    n, a, b = 0, 0, 1
    while n < max: 
        yield b #print -> yield 变成generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行
        a, b = b, a + b
        n = n + 1
    return 'done'
```

##### Iterator：

```python
it = iter([1, 2, 3, 4, 5])
x = next(it)
```

##### 高阶函数：

函数可以作为变量, 可以被返回（闭包）

匿名函数 `f = lambda x: x * x`

偏函数 `int2 = functools.partial(int, base=2)` 把某些变量默认固定

```python
map(lambda x:x*x, [1, 2, 3, 4, 5, 6, 7, 8, 9])
reduce(lambda (x,y):x+y, [1, 3, 5, 7, 9])
filter(is_palindrome, range(1, 200))
sorted([36, 5, -12, 9, -21], key=abs)
```

##### 装饰器 `@`

decorator就是一个返回函数的高阶函数

```python
@log
def now():
# 等价于log(now())
@log('execute')
def now():
#  等价于 log('execute')(now)

def log(text):
    def decorator(func):
        @functools.wraps(func) #函数签名纠正
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator
```



#### 常用用法

```
paths.split('/') if "://" not in paths else paths.split('|') # paths: str
```

```
    for k in itertools.count():
        # 如果combine=False 找到一个就结束 否则混合加载
        split_k = split + (str(k) if k > 0 else "") # split,split1,split2,...

        # infer langcode
        if split_exists(split_k, src, tgt, src, data_path):
            prefix = os.path.join(data_path, "{}.{}-{}.".format(split_k, src, tgt)) # train.zh.en-zh
        elif split_exists(split_k, tgt, src, src, data_path):
            prefix = os.path.join(data_path, "{}.{}-{}.".format(split_k, tgt, src))
        else:
            if k > 0:
                break
            else:
                raise FileNotFoundError(
                    "Dataset not found: {} ({})".format(split, data_path)
                )
```



```python
if not all(len(elem) == elem_size for elem in it):
```

抽奖

```
seed = int(茅台开盘价)
import numpy as np
np.random.seed(seed)
num = 参与人数
win = np.random.randint(1, num + 1)
print("中奖用户的抽奖码:", win)
```



#### 垃圾回收

主要使用引用计数（reference counting）来跟踪和回收垃圾。在引用计数的基础上，通过“标记-清除”（mark and sweep）解决容器对象可能产生的循环引用问题，通过“分代回收”（generation collection）以空间换时间的方法提高垃圾回收效率。

#### 进程线程

###### 多进程 multiprocessing

Python的`os`模块封装了常见的系统调用，其中就包括`fork`，可以在Python程序中轻松创建子进程：

```python
print('Process (%s) start...' % os.getpid())
pid = os.fork()# Only works on Unix/Linux/Mac:
if pid == 0:
    print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
else:
    print('I (%s) created a child process (%s).' % (os.getpid(), pid))
#Process (492) start...
#I (492) just created a child process (502).
#I am child process (502) and my parent is 492.
```

`multiprocessing`模块就是跨平台版本的多进程模块,提供了一个`Process`类来代表一个进程对象, `join()`方法可以等待子进程结束后再继续往下运行

```python
import multiprocessing
import os

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = multiprocessing.Process(target=run_proc, args=('test',))
    p.start() #Child process start.
    p.join() #Child process end.
```

启动大量的子进程，可以用进程池`Pool`的方式批量创建子进程：

```python
from multiprocessing import Pool
import os, time, random

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__=='__main__':
    p = Pool(4) #最多同时执行4个进程,所以有一个task结束后第5个task才会执行
    for i in range(5): # 0,1,2,3,4
        p.apply_async(long_time_task, args=(i,))
    p.close() # 调用join()之前必须先调用close()，调用close()之后就不能继续添加新的Process了。
    p.join()
```

外部子进程, 一般需要控制子进程的输入和输出, `subprocess`模块可以让我们非常方便地启动一个子进程，然后控制其输入和输出

```python
import subprocess

r = subprocess.call(['nslookup', 'www.python.org']) # 输出
print('Exit code:', r)

p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#  set q=mx ; 針對郵箱的mx記錄
output, err = p.communicate(b'set q=mx\npython.org\nexit\n') #输入
print(output.decode('utf-8'))
print('Exit code:', p.returncode)
```

进程间的通信: `multiprocessing`模块包装了底层的机制，提供了`Queue`、`Pipes`等多种方式来交换数据。

```python
from multiprocessing import Process, Queue
import os, time, random

# 写数据进程执行的代码:
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())

# 读数据进程执行的代码:
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)

if __name__=='__main__':
    q = Queue() # 父进程创建Queue，并传给各个子进程：
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pw.start() # 启动子进程pw，写入:
    pr.start() # 启动子进程pr，读取:
    pw.join() # 等待pw结束:
    pr.terminate() # pr进程里是死循环，无法等待其结束，只能强行终止:
```

###### 多线程 multithread

Python的线程是真正的Posix Thread，而不是模拟出来的线程。提供了两个模块：`_thread`和`threading`，`_thread`是低级模块，`threading`是高级模块，对`_thread`进行了封装。绝大多数情况下，我们只需要使用`threading`这个高级模块。

任何进程默认就会启动一个线程，我们把该线程称为主线程`MainThread`，主线程又可以启动新的线程

```python
import threading

# 新线程执行的代码:
def loop():
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
    print('thread %s ended.' % threading.current_thread().name) # LoopThread

t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()
print('thread %s ended.' % threading.current_thread().name) # MainThread
```

多线程和多进程最大的不同在于，多进程中，同一个变量，各自有一份拷贝存在于每个进程中，互不影响，而多线程中，所有变量都由所有线程共享，所以，任何一个变量都可以被任何一个线程修改，因此，线程之间共享数据最大的危险在于多个线程同时改一个变量，把内容给改乱了

```python
import threading

# 假定这是你的银行存款:
balance = 0
lock = threading.Lock()

def change_it(n):
    # 先存后取，结果应该为0:但实际不一定
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(2000000):
        change_it(n)

def run_thread_lock(n):
    for i in range(100000):
        lock.acquire()
        try:
            change_it(n)
        finally:
            lock.release() # 获得锁的线程用完后一定要释放锁，否则那些苦苦等待锁的线程将永远等待下去，成为死线程

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)
```

分析: 高级语言的一条语句在CPU执行时是若干条语句, `balance = balance + n`也分两步：

1. 计算`balance + n`，存入临时变量中；
2. 将临时变量的值赋给`balance`。

t1和t2是交替运行的，如果操作系统以下面的顺序执行t1、t2：

```python
初始值 balance = 0

t1: x1 = balance + 5  # x1 = 0 + 5 = 5

t2: x2 = balance + 8  # x2 = 0 + 8 = 8
t2: balance = x2      # balance = 8

t1: balance = x1      # balance = 5
t1: x1 = balance - 5  # x1 = 5 - 5 = 0
t1: balance = x1      # balance = 0

t2: x2 = balance - 8  # x2 = 0 - 8 = -8
t2: balance = x2      # balance = -8

结果 balance = -8
```

究其原因，是因为修改`balance`需要多条语句，而执行这几条语句时，线程可能中断，从而导致多个线程把同一个对象的内容改乱了

###### 线程和核

启动与CPU核心数量相同的N个线程，在4核CPU上可以监控到CPU占用率仅有102%，也就是仅使用了一核。但是用C、C++或Java来改写相同的死循环，直接可以把全部核心跑满，4核就跑到400%，8核就跑到800%，为什么Python不行呢？

因为Python的线程虽然是真正的线程，但解释器执行代码时，有一个GIL锁：`Global Interpreter Lock`，任何Python线程执行前，必须先获得GIL锁，然后，每执行100条字节码，解释器就自动释放GIL锁，让别的线程有机会执行。这个GIL全局锁实际上把所有线程的执行代码都给上了锁，所以，<u>多线程在Python中只能交替执行</u>，即使100个线程跑在100核CPU上，也只能用到1个核。

GIL是Python解释器设计的历史遗留问题，通常我们用的解释器是官方实现的CPython，要真正利用多核，除非重写一个不带GIL的解释器。

所以，在Python中，可以使用多线程，但不要指望能有效利用多核。如果一定要通过多线程利用多核，那只能通过C扩展来实现，不过这样就失去了Python简单易用的特点。

不过，也不用过于担心，Python虽然不能利用多线程实现多核任务，但可以通过多进程实现多核任务。多个Python进程有各自独立的GIL锁，互不影响。

###### Threadlocal



###### 多任务

多任务一旦多到一个限度，就会消耗掉系统所有的资源，结果效率急剧下降，所有任务都做不好

计算密集型任务由于主要消耗CPU资源，因此，代码运行效率至关重要。Python这样的脚本语言运行效率很低，完全不适合计算密集型任务。对于计算密集型任务，最好用C语言编写。

IO密集型，涉及到网络、磁盘IO，这类任务的特点是CPU消耗很少，任务的大部分时间都在等待IO操作完成（因为IO的速度远远低于CPU和内存的速度）。IO密集型任务执行期间，99%的时间都花在IO上，花在CPU上的时间很少，因此，用运行速度极快的C语言替换用Python这样运行速度极低的脚本语言，完全无法提升运行效率。对于IO密集型任务，最合适的语言就是开发效率最高（代码量最少）的语言，脚本语言是首选，C语言最差。

在Thread和Process中，应当优选Process，因为Process更稳定，而且，Process可以分布到多台机器上，而Thread最多只能分布到同一台机器的多个CPU上。

Python的`multiprocessing`中的`managers`子模块支持把多进程分布到多台机器上。一个服务进程可以作为调度者，将任务分布到其他多个进程中，依靠网络通信。由于`managers`模块封装很好，不必了解网络通信的细节，就可以很容易地编写分布式多进程程序



###### 补充

```python
if parallel:
    pool = mp.Pool(processes=mp.cpu_count())
    gs = pool.map(partial_worker, extract_range)
else:
    for i in extract_range:
        gs.append(partial_worker(i))  # NOTICE: non-parallel can help debug
```

# Link

- 基础练习： https://github.com/darkprinx/break-the-ice-with-python



- https://github.com/taizilongxu/interview_python
- https://github.com/kenwoodjw/python_interview_question
- https://github.com/hantmac/Python-Interview-Customs-Collection
- https://www.iamshuaidi.com/3036.html
- https://github.com/jackfrued/Python-Interview-Bible/blob/master/Python%E9%9D%A2%E8%AF%95%E5%AE%9D%E5%85%B8-%E5%9F%BA%E7%A1%80%E7%AF%87-2020.md



- https://github.com/khanhnamle1994/cracking-the-data-science-interview

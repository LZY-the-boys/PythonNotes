
##### 拷贝问题


赋值: 只是复制了新对象的引用 （从变量到对象的连接），不会开辟新的内存空间

浅拷贝: 仅只拷贝了一层，拷贝了最外围的对象本身，内部的元素都只是拷贝了一个引用而已
```python
lst1 = lst[:] # 切片操作
lst1 = [each for each in lst] # 切片操作
lst1 = list(lst) # 工厂函数
lst1 = copy.copy(lst) # copy函数
lst1 = lst.copy()
```

深拷贝：(`copy.deepcopy()`) 和浅拷贝对应，深拷贝拷贝了对象的所有元素，包括多层嵌套的元素。深拷贝出来的对象是一个全新的对象，不再与原来的对象有任何关联

不可变对象（字符串、元组、数值类型）的浅拷贝深拷贝和“赋值”的情况一样，
对象的id值（id()函数用于获取对象的内存地址）与浅复制原来的值相同

```python
import copy
a=(1,2,3)

print("=====赋值=====")
b=a
print(a)   # (1, 2, 3)
print(b)   # (1, 2, 3)
print(id(a))   # 43481128
print(id(b))   # 43481128

print("=====浅拷贝=====")
b=copy.copy(a)
print(a)    # (1, 2, 3)
print(b)    # (1, 2, 3)
print(id(a))    # 43481128
print(id(b))    # 43481128

print("=====深拷贝=====")
b=copy.deepcopy(a)
print(a)  # (1, 2, 3)
print(b)  # (1, 2, 3)
print(id(a))  # 43481128
print(id(b))  # 43481128

```

可变对象赋值： 值相等，地址相等， 拷贝值相等，地址不相等

```python

b=a  # =====赋值=====
print(a)  # [1, 2, 3]
print(b)  # [1, 2, 3]
print(id(a))  # 37235144
print(id(b))  # 37235144
b=copy.copy(a)   # =====浅拷贝=====
print(a)   # [1, 2, 3]
print(b)   # [1, 2, 3]
print(id(a))   # 37235144
print(id(b))   # 37191432
b=copy.deepcopy(a)    # =====深拷贝=====
print(a)    # [1, 2, 3]
print(b)    # [1, 2, 3]
print(id(a))    # 37235144
print(id(b))    # 37210184
```

然而关键在于 外层添加元素时，浅拷贝不会随原列表变化而变化；内层添加元素时，浅拷贝才会变化

```python
l=[1,2,3,[4, 5]]

l1=l #赋值
l2=copy.copy(l) #浅拷贝
l3=copy.deepcopy(l) #深拷贝
l[3].append(6) 

print(l1)
print(l2)
print(l3)

# [1, 2, 3, [4, 5, 6]]      
# [1, 2, 3, [4, 5, 6]]      #  赋值对象随着原列表一起变化
# [1, 2, 3, [4, 5, 6]]      #  浅拷贝外部不变，但内部会添加一个元素6
# [1, 2, 3, [4, 5]]         #  深拷贝保持不变

```

注意list的坑点： 
(1) `[[]]*n`  each element is the same list:
``` python 
d = [[]]*n
d[0].append(1)
#[[1],[1],...]

d = [[] for x in xrange(n)] # 正确写法 是浅拷贝
```
(2) `append` is not a copy
```
res = []
ans.append(res.copy())
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
# 按列遍历技巧
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
  - `+-*/` implement: `__add__, __radd__, __neg__`

  - `__slots__`变量，限制该class实例能添加的属性 可以起到加速的效果

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

Iterator：

```python
it = iter([1, 2, 3, 4, 5])
x = next(it)
```

reference: https://python-patterns.guide/gang-of-four/composition-over-inheritance/

proliferation of classes / subclass explosion: 
用继承同时实现两种不同功能(比如实现Logger的filter和file)，必然面对子类数目爆炸
解决方案是认识到既负责过滤消息又负责记录消息的类过于复杂。在现代面向对象实践中，它会被指责违反“单一职责原则”（Single Responsibility Principle）

- Adapter Pattern:
原始的Logger只需要一个泛文件的write接口 /FilteredLogger不变，实现封装write功能的 adapter
adapter和logger object可自由组合，就避免了子类爆炸
```python
import sys
import syslog

class Logger(object):
    def __init__(self, file):
        self.file = file

    def log(self, message):
        self.file.write(message + '\n')
        self.file.flush()
# write duck 
class FileLikeSocket:
    def __init__(self, sock):
        self.sock = sock

    def write(self, message_and_newline):
        self.sock.sendall(message_and_newline.encode('ascii'))

    def flush(self):
        pass

class FileLikeSyslog:
    def __init__(self, priority):
        self.priority = priority

    def write(self, message_and_newline):
        message = message_and_newline.rstrip('\n')
        syslog.syslog(self.priority, message)

    def flush(self):
        pass
```

- Bridge Pattern:
同样引入一个独立的类，Bridge模式是在设计时应用的，而Adapter模式在设计完成后用于兼容和匹配不匹配的接口。
Bridge被用来分离抽象接口(“abstractions”)和具体实现(“implementations”)。换句话说，我们可以在不改变抽象接口的同时更改实现。
```Python
# The “abstractions” that callers will see.
class Logger(object):
    def __init__(self, handler):
        self.handler = handler

    def log(self, message):
        self.handler.emit(message)

class FilteredLogger(Logger):
    def __init__(self, pattern, handler):
        self.pattern = pattern
        super().__init__(handler)

    def log(self, message):
        if self.pattern in message:
            super().log(message)

# The “implementations” hidden behind the scenes.
class FileHandler:
    def __init__(self, file):
        self.file = file

    def emit(self, message):
        self.file.write(message + '\n')
        self.file.flush()

class SocketHandler:
    def __init__(self, sock):
        self.sock = sock

    def emit(self, message):
        self.sock.sendall((message + '\n').encode('ascii'))

```

- Decorator Pattern
如果我们想对同一日志应用两个不同的过滤器——比如，一个按优先级过滤，另一个匹配关键字, 我们可以将过滤代码独立移出Logger之外，从而可以包装在我们想要的任何记录器上。

```Python
class LogFilter:
    def __init__(self, pattern, logger):
        self.pattern = pattern
        self.logger = logger

    def log(self, message):
        if self.pattern in message:
            self.logger.log(message)

log1 = FileLogger(sys.stdout)
log2 = LogFilter('Error', log1)
```

Real Python Logger Implementation：
- Logger类消息可能需要多个过滤器和多个输出——来完全解耦过滤器类和处理程序类:
- 调用者与之交互的Logger类本身并不实现过滤或输出。相反，它维护一个过滤器列表和一个处理程序列表
- 对于每个日志消息，日志记录器调用它的每个过滤器。如果任何过滤器拒绝该消息，则该消息将被丢弃。
- 对于所有过滤器都接受的每条日志消息，日志记录器循环遍历其输出处理程序，并调用它们各自的emit()

```Python
# There is now only one logger.
class Logger:
    def __init__(self, filters, handlers):
        self.filters = filters
        self.handlers = handlers

    def log(self, message):
        if all(f.match(message) for f in self.filters):
            for h in self.handlers:
                h.emit(message)

# Filters now know only about strings!
class TextFilter:
    def __init__(self, pattern):
        self.pattern = pattern

    def match(self, text):
        return self.pattern in text

# Handlers look like “loggers” did in the previous solution.
class FileHandler:
    def __init__(self, file):
        self.file = file

    def emit(self, message):
        self.file.write(message + '\n')
        self.file.flush()
```

Raw IF version:
```Python
class Logger:
    def __init__(self, pattern=None, file=None, sock=None, priority=None):
        self.pattern = pattern
        self.file = file
        self.sock = sock
        self.priority = priority

    def log(self, message):
        if self.pattern is not None:
            if self.pattern not in message:
                return
        if self.file is not None:
            self.file.write(message + '\n')
            self.file.flush()
        if self.sock is not None:
            self.sock.sendall((message + '\n').encode('ascii'))
        if self.priority is not None:
            syslog.syslog(self.priority, message)
```

if语句方法优点：
- 这个类的所有可能的行为都可以在从上到下的一次阅读代码中掌握。参数列表可能看起来很冗长，但由于Python的可选关键字参数，大多数对该类的调用都不需要提供所有四个参数。
缺点：
- 难以定位功能：如果您的任务是改进或调试一个特定的特性——比如，支持向套接字写入——您将发现无法在一个地方全部读取其代码。这个特性背后的代码分散在初始化器的参数列表、初始化器的代码和log()方法本身之间。
- 难以删除功能：从if语句林中删除套接字特性不仅需要小心避免破坏相邻的代码
- 效率低下，难以测试

Multiple Inheritance Version
```Python
class Logger(object):
    def __init__(self, file):
        self.file = file

    def log(self, message):
        self.file.write(message + '\n')
        self.file.flush()

class SocketLogger(Logger):
    def __init__(self, sock):
        self.sock = sock

    def log(self, message):
        self.sock.sendall((message + '\n').encode('ascii'))

class FilteredLogger(Logger):
    def __init__(self, pattern, file):
        self.pattern = pattern
        super().__init__(file)

    def log(self, message):
        if self.pattern in message:
            super().log(message)

# A class derived through multiple inheritance.
class FilteredSocketLogger(FilteredLogger, SocketLogger):
    def __init__(self, pattern, sock):
        FilteredLogger.__init__(self, pattern, None)
        SocketLogger.__init__(self, sock)
```

显然是错误的，优先调用的FilteredLogger的log方法，而且对于单元测试等检查具有很多坏处 https://python-patterns.guide/gang-of-four/composition-over-inheritance/


一种方法是用Mixin实现
```Python
# Simplify the filter by making it a mixin.
class FilterMixin:  # No base class!
    pattern = ''

    def log(self, message):
        if self.pattern in message:
            super().log(message)

# Multiple inheritance looks the same as above.

class FilteredLogger(FilterMixin, FileLogger):
    pass 
# super().log 将会调用 FileLogger.log
```
而且基于Multiple inheritance依然不能避免子类爆炸问题，还是得显式写出所有子类, 可以通过动态生成解决

```Python
filters = {
    'pattern': PatternFilteredLog,
    'severity': SeverityFilteredLog,
}
outputs = {
    'file': FileLog,
    'socket': SocketLog,
    'syslog': SyslogLog,
}
filter_cls = filters[filter_name]
output_cls = outputs[output_name]
name = filter_name.title() + output_name.title() + 'Log'
cls = type(name, (filter_cls, output_cls), {})

# or getattr
```
缺点：
- 可读性极差，难以静态分析和调试定位错误



## The Global Object Pattern

每个Python模块都是一个单独的命名空间。像json这样的模块可以提供一个loads()函数，而不会与pickle模块中定义的完全不同的loads()函数冲突、替换或覆盖。

1. Constant

常量通常是在重构时引入的: 程序员注意到相同的值60.0在他们的代码中反复出现，因此为该值引入了一个常量SSL_HANDSHAKE_TIMEOUT。
现在，每次使用该名称都会产生在全局作用域中进行搜索的轻微成本，
但这可以通过几个优点加以平衡。常量的名称现在记录了值的含义，提高了代码的可读性。并且常量的赋值语句现在提供了一个单独的位置，在这里可以在将来编辑值，而不需要为每个使用遍历代码

> “dunder” constants  除了官方的dunder常量`__name__` `__file__`之外，一些模块可能自己创建dunder常量。比如__author__和__version__等名称

2. Mutable global 

可变全局尽管存在很大的危险，但他有每个模块都可以访问的地方的便利，可以迅速联合位置很远的两个模块。
要注意不能在全局增加耗时操作（I/O操作）


3. Prebound Method Pattern

> "share state" 比如random的randrange(), randint(), and choice() 是用的同一个种子的，

```Python
from datetime import datetime

class Random8(object):
    def __init__(self):
        self.set_seed(datetime.now().microsecond % 255 + 1)

    def set_seed(self, value):
        self.seed = value

    def random(self):
        self.seed, carry = divmod(self.seed, 2)
        if carry:
            self.seed ^= 0xb8
        return self.seed

_instance = Random8()
random = _instance.random
set_seed = _instance.set_seed
```

还有pdb也是如此实现的

4. The Sentinel Object Pattern

该模式通常使用Python的内置None对象，但在None可能是有用值的情况下，可以使用唯一的哨兵对象()来指示丢失或未指定的数据。（这在Go里边非常常见）
```Python
i = a.find(b)
if i == -1: # sentinel value.
    return

if other_object is None:
    ...
```

```go
//  two-value return pattern
byte_count, err := fmt.Print("Hello, world!")
if err != nil {
        ...
}
```

和C/C++不同，Python无法用NULL/空指针判断，因为Python中的每个名称都是一个指针，都有有效地址
```C
PyObject *my_repr = PyObject_Repr(obj);
if (my_repr == NULL) {
     ...
}
```

当我们需要使用None（None是合法值）的场景下，
```Python
sentinel = object()  # unique object used to signal cache misses
result = cache_get(key, sentinel)
if result is not sentinel:
    ...
```

## Creational Pattern

1. Python支持送入Callable作为函数，所以天然可以实现factory的方法
```
def build_decimal(string):
    return Decimal(string)

print(json.loads(text, parse_float=build_decimal))
```

2. Abstract Factory Pattern
```Python

from abc import ABCMeta, abstractmethod

class AbstractFactory(metaclass=ABCMeta):

    @abstractmethod
    def build_sequence(self):
        pass

    @abstractmethod
    def build_number(self, string):
        pass

class Factory(AbstractFactory):
    def build_sequence(self):
        return []

    def build_number(self, string):
        return Decimal(string)

class Loader(object):
    def load(string, factory):
        sequence = factory.build_sequence()
        for substring in string.split(','):
            item = factory.build_number(substring)
            sequence.append(item)
        return sequence

f = Factory()
result = Loader.load('1.23, 4.56', f)
print(result)
```

3. The Builder Pattern

库需要提供尽可能精简的实例化调用代码，
- Requests库 声称其比 使用 旧的urllib2标准库模块 执行的相同操作的更少行数 
- pyplot 
```Python
class PortBuilder(object):
    def __init__(self, port):
        self.port = port
        self.name = None
        self.protocol = None

    def build(self):
        return Port(self.port, self.name, self.protocol)
```

4. The Factory Method Pattern

“工厂方法”模式不太适合Python。它是为功能不足的编程语言设计的，在这些语言中，类和函数不能作为参数传递或作为属性存储。在这些语言中，工厂方法是一种笨拙但必要的逃避途径。但是对于Python应用程序来说，这不是一个好的设计

Imagine that you were using a language where:

Classes are not first-class objects. You are not allowed to leave a class sitting around as an attribute of either a class instance or of another class itself.
Functions are not first-class objects. You’re not allowed to save a function as an instance of a class or class instance.
No other kind of callable exists that can be dynamically specified and attached to an object at runtime.
Under such dire constraints, you would turn to subclassing as a natural way to attach verbs — new actions — to existing classes, and you might use method overriding as a basic means of customizing behavior. 
And if on one of your classes you designed a special method whose only purpose was to isolate the act of creating new objects, then you’d be using the Factory Method pattern.

- Dependency Injection 依赖注入
```Python
import json
with open('input_data.json') as f:
    data = json.load(f)
```
用open f的形式，json.load事实上解耦了读取依赖，

- 直接送入callable作为参数
```Python
class JSONDecoder(object):
    ...
    def __init__(self, ... parse_float=None, ...):
        ...
        self.parse_float = parse_float or float
        ...

my_decoder = JSONDecoder(parse_float=Decimal)
```
如果开发人员不进行干预，则使用对float类型本身的快速调用来解释每个数字。如果开发人员提供了他们自己的可调用对象来解析数字，那么这个可调用对象就会被透明地使用。


4. The Prototype Pattern

Prototype模式在强大到足以支持一级函数和类的语言中是不必要的。

supplying a framework with a menu of classes that will need to be instantiated with pre-specified argument lists

Python提供了几种可能的机制来为框架提供我们想要实例化的类和我们想要实例化它们的参数
```
menu = {
    'whole note': lambda: Note(fraction=1),
    'half note': lambda: Note(fraction=2),
    'quarter note': lambda: Note(fraction=4),
    'sharp': Sharp,
    'flat': Flat,
}
```

5. The Singleton Pattern

单例类禁止正常的实例化，而是提供一个返回单例实例的类方法。Python允许类在定义一个返回单例实例的自定义__new__()方法时继续支持正常的实例化语法.如果您的设计迫使您提供对单例对象的全局访问，那么更python化的方法是使用 The Global Object Pattern 模式。

在面向对象设计模式社区定义“Singleton Pattern”之前，Python就已经在使用术语“singleton ”了 但他们有区别；https://python-patterns.guide/gang-of-four/singleton/
```Python
# Straightforward implementation of the Singleton Pattern

class Logger(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(Logger, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

log1 = Logger()
print(log1) # Creating the object
log2 = Logger()
print(log2) # same logger
```


## Structural Patterns


1. The Composite Pattern

Composite Pattern： 像ls、du和chmod这样的操作对file和dir上都有效，因此它们可以透明地在两者上运行
这种对称性——ls对单个文件和包含这些文件的目录均可运行——对大多数用户来说似乎是如此自然，以至于您可能没有注意到它背后强大的设计决策。

2. Decorator Pattern

> “Decorator Pattern” ≠ Python “decorators”!

Monkey Patch！

```Python
# peft package 的原理
class WriteLoggingFile3(object):
    def __init__(self, file, logger):
        self._file = file
        self._logger = logger

    # The two methods we actually want to specialize,
    # to log each occasion on which data is written.

    def write(self, s):
        self._file.write(s)
        self._logger.debug('wrote %s bytes to %s', len(s), self._file)

    def writelines(self, strings):
        if self.closed:
            raise ValueError('this file is closed')
        for s in strings:
            self.write(s)

    # Two methods we don't actually want to intercept,
    # but iter() and next() will be upset without them.

    def __iter__(self):
        return self.__dict__['_file'].__iter__()

    def __next__(self):
        return self.__dict__['_file'].__next__()

    # Offer every other method and property dynamically.

    def __getattr__(self, name):
        return getattr(self.__dict__['_file'], name)

    def __setattr__(self, name, value):
        if name in ('_file', '_logger'):
            self.__dict__[name] = value
        else:
            setattr(self.__dict__['_file'], name, value)

    def __delattr__(self, name):
        delattr(self.__dict__['_file'], name)
```

3. The Flyweight Pattern

缓存机制，每次不重新实例化相同的对象，而是返回之前的缓存的对象 (peft adapter 的调用)

```Python
class Grade(object):
    _instances = {}

    def __new__(cls, percent):
        percent = max(50, min(99, percent))
        letter = 'FDCBA'[(percent - 50) // 10]
        self = cls._instances.get(letter)
        if self is None:
            self = cls._instances[letter] = object.__new__(Grade)
            self.letter = letter
        return self

    def __repr__(self):
        return 'Grade {!r}'.format(self.letter)

print(Grade(55), Grade(85), Grade(95), Grade(100))
print(len(Grade._instances))    # number of instances
print(Grade(95) is Grade(100))  # ask for ‘A’ two more times
print(len(Grade._instances))    # number stayed the same?
```


## Behavioral Patterns

The Iterator Pattern Python的for循环将迭代器模式抽象得如此彻底，以至于大多数Python程序员甚至从未意识到它在表面之下所实施的对象设计模式。

- iter() takes a container object as its argument and asks it to build and return a new iterator object. 
  If the argument you pass isn’t actually a container, a TypeError is raised: object is not iterable.
- next() takes the iterator as its argument and, each time it’s called, returns the next item from the container. 
  Once the container has no more objects to return, the exception StopIteration is raised.

```Python
# for loop 
>>> it = iter(some_primes)
>>> it
<list_iterator object at 0x7f072ffdb518>
>>> print(next(it))
2
>>> print(next(it))
3
>>> print(next(it))
5
>>> print(next(it))
Traceback (most recent call last):
  ...
StopIteration
```

之所以需要将container和iterator分开实现，是因为一个对象可能同时被几个for循环操作，因此每个for循环也需要它们自己的迭代器，以避免彼此偏离轨道。
```Python
for i in lista:
    for j in lista:
        print(i,j)
```


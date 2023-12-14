
## 没有 try-except 机制的场景：类似于go的异常处理 

def func2(r):

    if r < 0:
        # error code
        return None
    return r - 1

def func1(r):

    # 一旦出错要一级一级上报，直到某个函数可以处理该错误（比如，给用户输出一个错误信息）。
    res = func2(r)
    if res is None:
        return None
    
    # do something
    return res - 1

def func0(r=None):

    res = func1(r)
    if res is None:
        # 最终可以处理错误的函数（比如，前端给用户输出一个错误信息）。
        print('you need input r > 0')
        return
    
    print(res)
        
## try-except 机制

def _func2(r):

    if r < 0:
        raise ValueError
    
    # do something
    return r -1 

def _func1(r):

    # 可以方便的跨多层调用
    res = _func2(r)    
    return res - 1

def _func0(r):

    try:
        res = _func1(r)
        print(res)
    except ValueError:
        print('you need input r > 0')

def _func00(r):
    # 如果错误没有被捕获，它就会一直往上抛，最后被Python解释器捕获，打印一个错误信息
    print(_func1(r))

def _func000(r):
    try:
        print(_func1(r))
    except:
        import sys,pdb,bdb
        type, value, tb = sys.exc_info()
        
        if type == bdb.BdbQuit:
            # 跳过pdb调试退出的exception
            exit()
        
        print(type,value)
        pdb.post_mortem(tb)

if __name__ == "__main__":
    _func000(int(input('input a r < 0 :')))
    # _func00(int(input('input a r < 0 :')))
    # _func0(int(input('input a r < 0 :')))
    # func0(int(input('input a r < 0 :')))



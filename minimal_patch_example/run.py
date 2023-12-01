

def fetch_thing():
    # query some database
    print('old')
    return 1

class Foo(object):
    def __init__(self):
        self.value = 0

    def bar(self):
        self.value = 100
        print("In original method")
        assert False
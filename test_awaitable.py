

class A:

    def __init__(self, get_co):
        self.__class__.ins = self
        self.get_co = get_co

    def wrapped(self):
        co = self.get_co()
        co.send(100)

    
    def __await__(self):
        yield self
        return 1



async def f(get_co):
    v = await A(get_co)
    print('v', v)

def run(f):
    
    def get_co():
        return co
    co = f(get_co)
    co.send(None)

if __name__ == '__main__':
    run(f)
    A.ins.wrapped()
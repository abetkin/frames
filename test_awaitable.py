
from contextlib import suppress

class Target:

    def method(self):
        return 1


class A:

    def __init__(self, get_co):
        self.get_co = get_co

    def wrap(self, _orig=Target.method):
        def wrapper(ins):
            ret = _orig(ins)
            co = self.get_co()
            with suppress(StopIteration):
                co.send(ret)
            return ret
        setattr(Target, 'method', wrapper)
        return wrapper

    
    def __await__(self):
        self.wrap()
        ret = (yield self)
        return ret



async def cofunc(A):
    v = await A
    print('spy: result =', v)


def run(f):
    def get_co():
        return co
    aa = A(get_co)
    co = f(aa)
    co.send(None)



class Importer(dict):
    ATTRS = [
        '_ns'
    ]

    def __init__(self, obj=None, attr=None):
        self.__dict__ = self
        self._ns.obj = obj
        self._ns.attr = attr

    def __getitem__(self, key):
        if key in Importer.ATTRS:
            return super().__getitem__(key)
        self._ns.attr = key
        


if __name__ == '__main__':
    run(cofunc)
    print('result =', Target().method())
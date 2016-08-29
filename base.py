from contextlib import suppress
from functools import wraps


class Patch:

    def __init__(self, co, attribute, parent):
        self.co = co
        self.parent = parent
        self.attribute = attribute
        self.original = getattr(self.parent, self.attribute, None)
        self.wrapper = self.make_wrapper(self.original)

    def on(self):
        setattr(self.parent, self.attribute, self.wrapper)

    def off(self):
        if self.original:
            setattr(self.parent, self.attribute, self.original)
        else:
            delattr(self.parent, self.attribute)
    
    def __await__(self):
        self.on()
        ret = (yield self)
        self.off()
        return ret


    def make_wrapper(self, wrapped):
        wrapped = self.original
        __self__ = getattr(wrapped, '__self__', None)
        if __self__:
             wrapped = wrapped.__func__

        @wraps(wrapped)
        def func(*args, **kwargs):
            ret = wrapped(*args, **kwargs)
            with suppress(StopIteration):
                self.co.send(ret)
            return ret

        if isinstance(__self__, type):
            func = classmethod(func)
        elif __self__:
            func = MethodType(func, __self__)
        return func



class Loco:
    def __init__(self, name):
        self.name = name
        func = getattr(self, name)
        self._co = func()
    
    def __call__(self, result):
        with suppress(StopIteration):
            self._co.send(None)
    
    def __matmul__(self, target):
        # FIXME
        container, attr = target
        return Patch(self._co, attr, container)
    
from contextlib import suppress
from functools import wraps

# rename: call
class Patch:

    def __init__(self, co, parent, attribute):
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
            # FIXME add import
            func = MethodType(func, __self__)
        return func


class Loco:
    # TODO: add unittest asserts

    def __init__(self, name):
        self.name = name
        func = getattr(self, name)
        self._gen_func = func
        self._gen = iter(self)

    def __call__(self, result):
        with suppress(StopIteration):
            p = self._gen.send(None)

    def __iter__(self):
        co = self._gen_func()
        with suppress(StopIteration):
            val = None
            while True:
                container, attr = co.send(val)
                p = Patch(self._gen, container, attr)
                p.on()
                val = (yield p)
                p.off()


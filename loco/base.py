from contextlib import suppress
from functools import wraps

# think about blinker

class Patch:

    # is listener for (container, func)
    # use target as a singleton (target.patched = True)

    def __repr__(self):
        return ' '.join((self.parent.__name__, self.attribute))

    def __init__(self, co, parent, attribute,
                 type='exit'):
        assert type in ['enter', 'exit']
        self.type = type
        self.co = co # FIXME co is a listener
        self.parent = parent
        self.attribute = attribute
        self.original = getattr(self.parent, self.attribute, None)
        
        # listeners = [(self.co, self.type)]
        # if not getattr(self.original, 'listeners', None):
        #     setattr(self.original, 'listeners', listeners)

        # else:
        #     self.original.listeners.extend(listeners)
        self.wrapper = self.make_wrapper(self.original)


    def on(self):
        # patch if no listeners
        # add listener
        target = self.original
        
        if not getattr(target, 'listeners', None):
            setattr(self.parent, self.attribute, self.wrapper)
            if not getattr(target, 'listeners', None):
                target.listeners = []
        target.listeners.append(self)
            

    def off(self):
        # remove listener
        # if no listeners, unpatch
        target = self.original
        target.listeners.remove(self)
        if not target.listeners:
            setattr(self.parent, self.attribute, self.original)

    def __or__(self, other):
        return AnyCall(self, other)

    # def hook(self, ret, call_info):
    #     call_info.ret = ret
    #     self.co.send(call_args)

    def make_wrapper(self, wrapped):
        wrapped = self.original
        __self__ = getattr(wrapped, '__self__', None)
        if __self__:
             wrapped = wrapped.__func__

        @wraps(wrapped)
        def func(*args, **kwargs):
            call_args = CallInfo(wrapped, args, kwargs)
            for p in wrapped.listeners:
                import ipdb; ipdb.set_trace()
                if p.type == 'enter':
                    with suppress(StopIteration):
                        p.co.send(call_args)
                        # AnyCall: here all patches should be unapplied
            ret = wrapped(*args, **kwargs)
            for p in wrapped.listeners:
                if p.type == 'exit':
                    with suppress(StopIteration):
                        call_args.ret = ret
                        p.co.send(call_args)
            return ret
        
        if isinstance(__self__, type):
            func = classmethod(func)
        elif __self__:
            # FIXME add import
            func = MethodType(func, __self__)
        return func


class AnyCall(object):
    def __init__(self, *calls):
        self.calls = calls
    
    def resolve(self, call, call_info):
        self.call = call
        self.call_info = call_info
    
    @property
    def which(self):
        return self.calls.index(self.call)




import inspect

class CallInfo:

    def __init__(self, func, args, kwargs, ret=NotImplemented):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._signature = inspect.signature(func)
        self.bound_args = self._signature.bind(*args, **kwargs).arguments
        self.ret = ret


    def __getitem__(self, key):
        if isinstance(key, int):
            return self.args[key]
        value = self.bound_args.get(key, NotImplemented)
        if value is not NotImplemented:
            return value
        value = self._signature.parameters.get(key, NotImplemented)
        if value is not NotImplemented:
            return value
        return KeyError(key)

    def __repr__(self):
        def pairs():
            for name, parameter in self._signature.parameters.items():
                value = self.bound_args.get(name, parameter.default)
                yield "%s=%s" % (name, value)
        return '(%s)' % ', '.join(pairs())

    def __iter__(self):
        if self.ret is not NotImplemented:
            yield self.ret
        yield from self.args




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

    def call(self, container, attr):
        return Patch(self._gen, container, attr)

    def enter(self, container, attr):
        return Patch(self._gen, container, attr, type='enter')
    
    def exit(self, container, attr):
        return Patch(self._gen, container, attr)

    def __iter__(self):
        co = self._gen_func()
        with suppress(StopIteration):
            val = None
            while True: #?
                value = co.send(val)
                if isinstance(value, AnyCall):
                    for i, p in enumerate(value.calls):
                        p.on()
                    val = (yield)
                    options = [p.original for p in value.calls]
                    which = options.index(val.func)
                    value.resolve(value.calls[which], val)
                    
                    val = value, val
                    # val.func is value.calls[2].original

                    for p in value.calls:
                        p.off()
                    continue

                    


                p = value
                # container, attr = co.send(val)
                import ipdb
                with ipdb.launch_ipdb_on_exception():
                    p.on()
                    val = (yield)
                    p.off()



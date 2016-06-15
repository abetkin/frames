def func():
    obj = yield from F.Klass.method(arg, **kw)
    print(obj)
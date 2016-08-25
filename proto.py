
class Target:

    def incr(self, value):
        return value + 1

class Awaited:
    def __init__(self, obj_path=None, parent_path=None, attr=None):
        self.obj_path = obj_path
        self.parent_path = parent_path
        self.attr = attr
    def __getattr__(self, key):
        if self.obj_path:
            path = '.'.join((self.obj_path, key))
        else:
            path = key
        return self.__class__(path, self.obj_path, key) 

    def __await__(self):
        # FIXME
        obj = __import__(self.obj_path)
        parent = __import__(self.parent_path)
        new_obj = self.wrap(obj)
        setattr(parent, self.attr, obj)
        yield self

A = Awaited()

def test():
    data = await F.Target.incr


if __name__ == '__main__':
    1
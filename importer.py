

class Importer(dict):
    ATTRS = [
        '_ns'
    ]

    class NS:
        pass

    def __init__(self, obj_path=None, attr=None):
        self.__dict__ = self
        self._ns = self.NS()
        self._ns.obj_path = obj_path or ''
        self._ns.attr = attr

    def __getitem__(self, key):
        if key in Importer.ATTRS:
            return super().__getitem__(key)
        if not self._ns.obj_path:
            assert not self._ns.attr
            self._ns.obj_path = key
        else:
            if self._ns.attr:
                self._ns.obj_path = '.'.join(self._ns.attr, self._ns.attr)
            self._ns.attr = key
        
    def eval(self):
        parent = __import__(self._ns.obj_path)
        obj = getattr(parent, self._ns.attr)
        return obj


if __name__ == '__main__':
    I = Importer()
    importer = I.mod.Klass.method
    print('imported', importer.eval())
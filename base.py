class Loco:
    def __init__(self, name):
        self.name = name
        func = getattr(self, name)
        self._co = func()
    
    def __call__(self, result):
        self._co.send(None)
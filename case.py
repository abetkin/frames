class Case(object):
    

    def __init__(self, name):
        self.name = name

    def __call__(self, *args):
        m = getattr(self, self.name)
        return m(*args)
from unittest.main import TestProgram as _TestProgram, loader

import inspect

from .base import Loco

class ActivateLocos(_TestProgram):
    def __init__(self, *args, **kwargs):
        loader = LocoLoader()
        kwargs.update({
            'testLoader': loader,
            'module': None,
            'exit': False,
        })
        super().__init__(*args, **kwargs)


class LocoLoader(loader.TestLoader):

    def getTestCaseNames(self, loco_class):
        def get_names():
            for name in dir(loco_class):
                val = getattr(loco_class, name, None)
                if inspect.iscoroutinefunction(val):
                    yield name
        return sorted(get_names())

    def loadTestsFromTestCase(self, loco_class):
        testCaseNames = self.getTestCaseNames(loco_class)
        locos = map(loco_class, testCaseNames)
        loaded_suite = self.suiteClass(locos)
        return loaded_suite

    def loadTestsFromModule(self, module, *args, pattern=None, **kws):
        tests = []
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, Loco):
                tests.extend(self.loadTestsFromTestCase(obj))
        return self.suiteClass(tests)

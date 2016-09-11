from unittest.main import TestProgram as _TestProgram, loader

import inspect
import sys

from fnmatch import fnmatch

from .base import Loco

class DiscoverLocos(_TestProgram):
    def __init__(self, *args, **kwargs):
        loader = LocoLoader()
        kwargs.update({
            'testLoader': loader,
            'module': None,
            'exit': False,
        })
        sys_argv = sys.argv[:]
        try:
            sys.argv[1:] = ['discover']
            super().__init__(*args, **kwargs)
        finally:
            sys.argv = sys_argv
        


class LocoLoader(loader.TestLoader):

    PATTERN = 'loco_*'

    def getTestCaseNames(self, loco_class):
        def get_names():
            for name in dir(loco_class):
                val = getattr(loco_class, name, None)
                if inspect.isgeneratorfunction(val) \
                        and fnmatch(name, self.PATTERN):
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

    # TODO loadFromName

    def discover(self, start_dir, pattern=None, top_level_dir=None):
        pattern = self.PATTERN
        return super().discover(start_dir, pattern, top_level_dir)

from unittest.main import TestProgram as _TestProgram

import inspect

from . import Loco

class ActivateLocos(_TestProgram):

    def __init__(self, *args, **kwargs):
        loader = LocoLoader()
        kwargs['testLoader'] = loader
        super(TestProgram, self).__init__(*args, **kwargs)


class LocoLoader(loader.TestLoader):

    def getTestCaseNames(self, loco_class):
        def get_names():
            for name in dir(loco_class):
                val = getattr(loco_class, name, None)
                if inspect.iscoroutinefunction(val):
                    yield val
        return sorted(get_names())

    def loadTestsFromTestCase(self, loco_class):
        testCaseNames = self.getTestCaseNames(loco_class)
        locos = []
        for name in testCaseNames:
            locofunc = getattr(loco_class, name, None)
            co = locofunc()
            def get_co():
                return co
            locos.append(co)

        loaded_suite = self.suiteClass(locos)
        return loaded_suite

    def loadTestsFromModule(self, module, *args, pattern=None, **kws):
        tests = []
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, Loco):
                tests.append(self.loadTestsFromTestCase(obj))
        return tests

    # FIXME loadFromName




class LocoRunner(object):

    # resultclass = TextTestResult

    def __init__(self, stream=None, descriptions=True, verbosity=1,
                 failfast=False, buffer=False, resultclass=None, warnings=None,
                 *, tb_locals=False):
        pass

    def run(self, loco):
        # FIXME
        loco.send(None)
        def get_co():
            return co
        loco(get_co)


# class Suite(object):
#     def __init__(self, co_items):
#         self.co_items = co_items

#     def __call__(self):
#         'FIXME'
#         for co in self.co_items:
#             co.send(None)
#         main = klass.main
#         main()

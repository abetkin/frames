from unittest.main import TestProgram as _TestProgram, loader

# FIXME
from case import Case

class TestProgram(_TestProgram):

    def __init__(self, *args, **kwargs):
        loader = CoLoader()
        kwargs['testLoader'] = loader
        super(TestProgram, self).__init__(*args, **kwargs)


class CoLoader(loader.TestLoader):

    def getTestCaseNames(self, testCaseClass):
        """Return a sorted sequence of method names found within testCaseClass
        """

        def isCoro(attrname, testCaseClass=testCaseClass, prefix='co_'):
            return attrname.startswith(prefix) and \
                callable(getattr(testCaseClass, attrname))
        testFnNames = list(filter(isTestMethod, dir(testCaseClass)))
        # if self.sortTestMethodsUsing:
        #     testFnNames.sort(key=functools.cmp_to_key(self.sortTestMethodsUsing))
        return sorted(testFnNames)

    def suiteClass(self, tests):
        return Suite(tests)
    
    def loadTestsFromTestCase(self, testCaseClass):
        testCaseNames = self.getTestCaseNames(testCaseClass)
        if not testCaseNames and hasattr(testCaseClass, 'runTest'):
            testCaseNames = ['runTest']
        loaded_suite = self.suiteClass(map(testCaseClass, testCaseNames))
        return loaded_suite

    def loadTestsFromModule(self, module, *args, pattern=None, **kws):
        tests = []
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, Case):
                tests.append(self.loadTestsFromTestCase(obj))

        return tests




class MFRunner(object):

    # resultclass = TextTestResult

    def __init__(self, stream=None, descriptions=True, verbosity=1,
                 failfast=False, buffer=False, resultclass=None, warnings=None,
                 *, tb_locals=False):
        pass

    def run(self, item):
        "Run the given test case or test suite."
        item()


class Suite(object):
    def __init__(self, co_items):
        self.co_items = co_items
    
    def __call__(self):
        'FIXME'
        for co in self.co_items:
            co.send(None)
        main = klass.main
        main()

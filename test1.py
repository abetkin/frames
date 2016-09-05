from loco import Loco
from logic import DoLogic

import unittest

class Suite1(unittest.TestCase):

    def test1(self):
        ret = yield DoLogic, 'method'
        print('test1: method returned', ret)
        return ret


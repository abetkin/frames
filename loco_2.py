from loco import Loco
from logic import DoLogic

class Suite2(Loco):
    
    def loco_1(self):
        ret = yield self.call(DoLogic, '__init__')
        print('__init__ returned', ret)
        return ret
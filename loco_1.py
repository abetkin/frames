from loco import Loco
from logic import DoLogic

class Suite1(Loco):
    
    def loco_1(self):
        ret = yield DoLogic, 'method'
        print('method returned', ret)
        return ret
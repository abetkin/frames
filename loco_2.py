from loco import Loco
from logic import DoLogic

class Suite2(Loco):

    # async def loco(self):
    #     ret = await (self@(DoLogic, '__init__'))
    #     print('__init__ returned', ret)
    #     return ret
    
    def loco_1(self):
        ret = yield DoLogic, '__init__'
        print('__init__ returned', ret)
        return ret
from loco import Loco
from .logic import DoLogic

class Suite1(Loco):

    async def loco(self):
        ret = await (self@(DoLogic, '__init__'))
        print('__init__ returned', ret)
        return ret
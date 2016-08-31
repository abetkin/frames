from loco import Loco
from .logic import DoLogic

class Suite1(Loco):

    async def loco1(self):
        ret = await (self@(DoLogic, 'method'))
        print('method returned', ret)
        return ret
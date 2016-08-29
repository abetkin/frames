
from .logic import DoLogic

from .base import Loco

class Suite1(Loco):

    def co_1(self):
        ret = yield DoLogic, 'method'
        print('returned', ret)
        return ret



print(__name__)

if __name__ == '__main__':
    from .main import ActivateLocos
    
    ActivateLocos()
    l = DoLogic()
    
    l.method()


from loco import Loco
from logic import DoLogic

class Suite1(Loco):
    
    # def loco_1(self):
    #     ret = yield self.call(DoLogic, 'method')
    #     print('method returned', ret)
    #     return ret


    
    def loco_any(self):
        while True:
            ret = yield (
                self.call(DoLogic, 'method') |
                self.call(DoLogic, 'm2')
            )
            if ret.which == 0:
                print('method returned', ret)
            elif ret.which == 1:
                print('method returned', ret)
        print('Finished')

# TODO self.enter() self.exit()
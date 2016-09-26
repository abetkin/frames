
import sys

from loco.base import AnyCall, Loco, Patch

def incr(x):
    return x + 1

class DoCalc(object):
    def __new__(self, x):
        return incr(x)

    # def main(self, x):
    #     return incr(x)

class L(Loco):


    def loco_1(self):
        events = [
            self.enter(DoCalc, '__new__'),
            self.exit(DoCalc, '__new__'),
            self.exit(sys.modules[__name__], 'incr'),
            self.enter(sys.modules[__name__], 'incr'),
        ]
        while 1:
            e = yield AnyCall(*events)
            print(e)

    # def loco_main(self):
    #     import ipdb; ipdb.set_trace()
    #     info = yield self.call(DoCalc, 'main')
    #     print(info)


if __name__ == '__main__':
    from loco_enter_exit import DoCalc
    r = DoCalc(2)
    # import ipdb; ipdb.set_trace()
    print("2 + 1 = %s" % r)


from loco import Loco

from pony.orm.sqltranslation import SQLTranslator, Monad

from loco.base import AnyCall, Loco, Patch

from pony.orm import *

class Ex(Loco):

    # def loco_1(self):
    #     while True:
    #         call = yield SQLTranslator, 'call'
    #         print('call returned', call)

    def loco_dispatch(self):
        indent = 0
        while True:
            ret = yield AnyCall(
                self.enter(SQLTranslator, 'dispatch'),
                self.exit(SQLTranslator, 'dispatch'),
            )
            translator, node, *_ = ret
            if ret.which == 0:
                print('{}{}'.format(' ' * indent, node))
                indent += 2
            else:
                indent -= 2

    
    # def loco_monads(self):
    #     while True:
    #         _, [m, *_] = yield Monad, '__init__'
    #         print(m)



if __name__ == '__main__':
    
    from pony.orm import *
    
    db = Database('sqlite', ':memory:')

    class Animal(db.Entity):
        kind = Required(str)
        traits = Optional(str)

    db.generate_mapping(create_tables=True)

    with db_session:
        Animal(kind='bear')

        bears = select(b.traits for b in Animal if b.kind.startswith('b'))
        print(bears[:])

        # select(
        #     b for b in Animal
        # )


from loco import Loco

from pony.orm.sqltranslation import SQLTranslator

class Ex(Loco):

    def loco_1(self):
        while True:
            call = yield SQLTranslator, 'call'
            print('call returned', call)

    def loco_2(self):
        ast = yield SQLTranslator, 'construct_sql_ast'
        print('ast', ast)



if __name__ == '__main__':
    
    from pony.orm import *
    
    db = Database('sqlite', ':memory:')

    class Bear(db.Entity):
        name = Required(str)

    db.generate_mapping(create_tables=True)

    with db_session:
        Bear(name='Umka')

        bears = select(b.name for b in Bear if b.name.startswith('U'))
        print(bears[:]) 
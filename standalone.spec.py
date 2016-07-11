
import my

from shortcuts import I

# named tuple and a dict

import cached_property

class Case(my.Case):

    @cached_property
    def ctx(self):
        return {}

    async def co_1(self):
        (ret, args, kw) = await I.module.Klass.method[:]
        kwarg = await I.module.Klass.method['kwarg']

    async def co_2(self):
        1
    

    # ordered ?
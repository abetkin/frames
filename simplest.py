'''
1. PoC test
2. PoC await
'''

class C(object):
    def __getattr__(self, name):
        1


async def co_custom():
    await C.Class.m
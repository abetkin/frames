

class Tst:
    async def setUp(self):
        await C.start
        self.started = 1

    async def dbg_feat(self):
        instance, * = await C.mod.Klass.method
        self.assertTrue(instance)
    
    async def dbg_2(self):
        arg, * = await C.other.Klass.__init__

    @classmethod
    def run(cls):
        # testsuite
        import main
        main.run()
    
    @classmethod
    def run2(cls):
        1


async def dbg_feat():
    # where to group into ?
    instance, * = await C.mod.Klass.method
    U.assertTrue(instance)

def test_feat():
    import main
    main.run()



from .base import Loco


class Suite1(Loco):

    async def loco1(self):
        print('lo co')


if __name__ == '__main__':
    import ipdb
    with ipdb.launch_ipdb_on_exception():
        from main import ActivateLocos

        ActivateLocos()


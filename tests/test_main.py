import unittest


class TestMain(unittest.TestCase):
    @unittest.skip("This module is main module")
    def test_1(self):
        pass

    @unittest.skip("It can't be tested")
    def test_2(self):
        pass

    @unittest.skip("Due to some extraordinary logic")
    def test_3(self):
        pass

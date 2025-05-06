import unittest
from constants import COLORS
from dbm import DEBUG


class TestConstants(unittest.TestCase):

    def test_colors(self):
        self.assertEqual(30, len(COLORS))

    @unittest.skip("It's constants")
    def test_const_skip1(self):
        pass

    @unittest.skip("It's constants")
    def test_const_skip2(self):
        pass

    @unittest.skip("It's constants")
    def test_const_skip3(self):
        pass


class TestDbm(unittest.TestCase):

    def test_false(self):
        self.assertEqual(False, DEBUG.get_flag())

    def test_true(self):
        DEBUG.switch_debug()
        self.assertEqual(True, DEBUG.get_flag())

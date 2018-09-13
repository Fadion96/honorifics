import unittest

from honorifics.textswapper import TextSwapperInMark


class TestSwapperInMark(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.swapper = TextSwapperInMark()

    def test_swap(self):
        self.assertEqual('text{*}{*A}text{*}B{*}text', self.swapper.swap('text{*}A{*}text{*}{*B}text'),
                         'swap with surroundings')

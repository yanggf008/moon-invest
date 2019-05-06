# coding: utf8
import unittest
from tools.okex_action import *


class TestOkexAction(unittest.TestCase):

    def test_get_currencies(self):
        c_list = get_currencies()
        self.assertIsInstance(c_list, list, "The return value of get_currencies() should be a list")
        self.assertGreater(len(c_list), 1, "The number of currencies should be greater than 1")


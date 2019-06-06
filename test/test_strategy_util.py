# coding: utf-8

import unittest
from tools.strategy_util import *


class TestStrategyUtil(unittest.TestCase):
    def test_get_hundred_list(self):
        hundred_list = get_hundred_list()
        print(hundred_list)
        self.assertIsNotNone(hundred_list)
        self.assertIsInstance(hundred_list, list, "hundred_list should be list type")

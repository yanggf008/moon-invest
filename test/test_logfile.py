# coding: utf-8
import unittest
from tools.get_logfile_name import *


class TestLogfile(unittest.TestCase):

    def test_system_logfile(self):
        system_logfile = get_system_logfile()
        self.assertEqual(system_logfile[:6], "system",
                         "The beginning of system logfile should be 'system'")

    def test_fifteen_logfile(self):
        fifteen_logfile = get_fifteen_logfile()
        self.assertEqual(fifteen_logfile[:15], "fifteenStrategy",
                         "The beginning of fifteen logfile should be 'fifteenStrategy'")

    def test_base_logfile(self):
        base_logfile = get_base_logfile()
        self.assertEqual(base_logfile[:4], "base",
                         "The beginning of base logfile should be 'base'")

    def test_fund_logfile(self):
        fund_logfile = get_fund_logfile()
        self.assertEqual(fund_logfile[:4], "fund",
                         "The beginning of fund logfile should be 'fund'")

    def test_action_logfile(self):
        action_logfile = get_action_logfile()
        self.assertEqual(action_logfile[:6], "action",
                         "The beginning of action logfile should be 'action'")


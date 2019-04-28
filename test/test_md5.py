# coding: utf8
import unittest
from tools.md5 import Md5tools


class TestMd5(unittest.TestCase):
    def test_sign_value(self):
        data_map = {"api_key": "YOUR_APIKEY", "secretkey": "YOUR_SECRETKEY"}
        sign_value_okex = Md5tools.get_sign_value(data_map)
        self.assertEqual(sign_value_okex, "57A4E450D62D0FA5FB111D4413CDE925",
                         "simple sign md5 value should be equal")

    def test_full_value(self):
        data_map = {"api_key": "YOUR_APIKEY", "secretkey": "YOUR_SECRETKEY"}
        full_value_okex = Md5tools.get_full_sign_value(data_map)
        self.assertEqual(full_value_okex, "3273B4DD631A8CA7C5AC8586C9F4FF1F",
                         "full sign md5 value should be equal")

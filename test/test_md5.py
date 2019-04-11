# coding: utf8
import unittest
from tools.md5 import Md5tools


class TestMd5(unittest.TestCase):
    def test_md5_value(self):
        data_map = {"api_key": "YOUR_APIKEY", "secretkey": "YOUR_SECRETKEY"}
        md5_value_okex = Md5tools.get_sign_value(data_map)
        self.assertEqual(md5_value_okex, "57A4E450D62D0FA5FB111D4413CDE925")

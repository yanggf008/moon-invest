# coding: utf8
import unittest
from tools.future import FutureAPI


class TestFurture(unittest.TestCase):
    def test_get_account(self):
        future = FutureAPI()
        print(future.get_coin_account("BTC"))
        print(future.get)
        # TODO: test under normal wifi
        future.take_order(client_oid="guofengyang", instrument_id="BTC-USD-190719", otype="1", price="10430", size="0.183", match_price="1", leverage="10")
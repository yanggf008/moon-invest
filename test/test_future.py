# coding: utf8
import unittest
from tools.future import FutureAPI


class TestFurture(unittest.TestCase):
    def test_get_account(self):
        future = FutureAPI()
        print(future.get_coin_account("BTC"))
        # TODO: test under normal wifi
        # size 1 is 0.01
        instrument_id = "BTC-USD-190726"
        future.cancel_uncomplete_orders(instrument_id)
        print(future.get_position())

        # future.take_order(client_oid="guofengfdfd", instrument_id="BTC-USD-190726", otype="1", price="10270", size="10", match_price="0", leverage="10")
        # future.market_close_all(instrument_id="BTC-USD-190726", direction="long")

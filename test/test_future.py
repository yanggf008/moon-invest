# coding: utf8
import unittest
from tools.future import FutureAPI


class TestFurture(unittest.TestCase):
    def test_get_account(self):
        future = FutureAPI()
        isinstance(future.get_coin_account("BTC"), map)
        # print(future.get_coin_account("BTC"))
        # size 1 is 0.01
        instrument_id = "BTC-USD-190927"
        future.cancel_uncomplete_orders(instrument_id)
        isinstance(future.get_position(), map)
        # print(future.get_position())
        assert(future.get_BTC_long_avail_qty() >= 0)
        # print(future.get_BTC_long_avail_qty())
        # future.take_order(client_oid="guofengfdfd", instrument_id="BTC-USD-190726", otype="1", price="10270", size="10", match_price="0", leverage="10")
        # future.market_close_all(instrument_id="BTC-USD-190726", direction="long")

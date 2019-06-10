# coding: utf-8
import unittest
from tools.spot import *
from tools.time_util import *


class TestSpot(unittest.TestCase):

    def test_get_kline(self):
        spot = Spot()
        instrument = "BTC-USDT"
        start = get_previous_utc(3)
        end = get_utc_timestamp()
        granularity = 7200
        klines = spot.get_kline(instrument, start, end, granularity)
        # for kline in klines:
        #     print(kline)
        self.assertIsNotNone(klines, "the return kline should not be None")

    def test_get_orders_list(self):
        spot = Spot()
        instrument_id = "R-USDT"
        orders_list_filled = spot.get_orders_list('filled', instrument_id)
        orders_list_open = spot.get_orders_list('open', instrument_id)
        self.assertIsInstance(orders_list_filled, list, "orders list should be list")
        self.assertIsInstance(orders_list_open, list, "orders list should be list")

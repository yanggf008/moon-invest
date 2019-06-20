# coding: utf8

from tools.strategy_util import *
from tools.kline_util import *


def down_five_sell(instrument_id):
    """
    Sell if top pattern formed and today price is down five average
    :param instrument_id: the id of the instrument
    :return: True or False(down five sell)
    """
    processed_klines = get_processed_klines(5, instrument_id, 86400)
    if is_down_five(instrument_id) and is_top_pattern(processed_klines[-3], processed_klines[-2], processed_klines[-1]):
        return True
    else:
        return False

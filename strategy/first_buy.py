# coding: utf8
from tools.strategy_util import *
from tools.kline_util import *


def check_hundred_buy(instrument_id):
    """
    There is a top kline within 5 days, and now price is under five average
    :param instrument_id: the name of instrument
    :return: True or False (buy or not)
    """
    if was_hundred_five(instrument_id) and is_down_five(instrument_id):
        return True
    else:
        return False

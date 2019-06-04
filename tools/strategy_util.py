# coding: utf8

from tools.kline_util import *
from tools.get_logfile_name import *
from tools.logfile import Logfile


# the examined kxians' length
KLEN = 10
# the period of forbid loss configuration
FIVEZHISUNTYPE = "1day"


def is_bottom_buy():
    logfile = Logfile(get_system_logfile())
    processedKxian = get_processed_klines(KLEN)
    x = processedKxian[-3]
    y = processedKxian[-2]
    z = processedKxian[-1]
    if is_bottom_pattern(x, y, z) is True:
        logfile.write_logfile("difenxingBUY:TRUE")
        return True
    else:
        logfile.write_logfile("difenxingBUY:FALSE")
        return False


def bottom_fail_sell():
    logfile = Logfile(get_system_logfile())
    processedKxian = get_processed_klines(KLEN)
    x = processedKxian[-3]
    y = processedKxian[-2]
    z = processedKxian[-1]
    if bottom_pattern_fail(x, y, z) is True:
        logfile.write_logfile("difenxingFailSELL:TRUE")
        return True
    else:
        logfile.write_logfile("difenxingFailSELL:FALSE")
        return False


def is_top_sell():
    logfile = Logfile(get_system_logfile())
    processedKxian = get_processed_klines(KLEN)
    x = processedKxian[-3]
    y = processedKxian[-2]
    z = processedKxian[-1]
    if is_top_pattern(x, y, z) is True:
        logfile.write_logfile("dingfenxingSELL:TRUE")
        return True
    else:
        logfile.write_logfile("dingfenxingSELL:FALSE")
        return False


def top_fail_buy(processed_klines):
    """
    This function to judge whether the top pattern fails
    :param processed_klines: the processed klines
    :return: True or False of top fail
    """
    logfile = Logfile(get_system_logfile())
    processedKxian = processed_klines
    x = processedKxian[-3]
    y = processedKxian[-2]
    z = processedKxian[-1]
    if top_pattern_fail(x, y, z) is True:
        logfile.write_logfile("dingfenxingFailBUY:TRUE")
        return True
    else:
        logfile.write_logfile("dingfenxingFailBUY:FALSE")
        return False


def is_stop_loss(price, rate, instrument_id):
    """
    Whether to stop loss
    :param price: the previous buy price
    :param rate: the stop loss rate
    :param instrument_id: the instrument name
    :return: True or False to stop loss
    """
    system_logfile = Logfile(get_system_logfile())
    spot = Spot()
    stop_price = float(price * (1 - float(rate)))
    current_buy_price = spot.get_buy_price(instrument_id)
    if current_buy_price < stop_price:
        system_logfile.write_logfile("3%ZhiSun:TRUE")
        return True
    else:
        system_logfile.write_logfile("3%ZhiSun:FALSE")
        return False


def get_five_average(instrument_id):
    """
    This function is to get the five average close price
    :param instrument_id: the instrument name
    :return: (float) value of five average
    """
    sumvalue = 0.0
    spot = Spot()
    for i in range(5):
        sumvalue = sumvalue + \
                   float(spot.get_kline(instrument_id, get_previous_utc(10),
                                        get_utc_timestamp(), 864000)[-1-i].close)
    return sumvalue / 5


def is_up_five(instrument_id):
    """
    Whether the current price is up five average price
    :param instrument_id: the instrument name
    :return: True or False of being up five
    """
    spot = Spot()
    system_logfile = Logfile(get_system_logfile())
    if float(spot.get_buy_price(instrument_id)) > get_five_average(instrument_id):
        system_logfile.write_logfile("upFIVE:TRUE")
        return True
    else:
        system_logfile.write_logfile("upFIVE:FALSE")
        return False


def is_down_five(instrument_id):
    """
    Whether the current price is under fiver average price
    :param instrument_id: the instrument name
    :return: True or False of being down five average
    """
    spot = Spot()
    system_logfile = Logfile(get_system_logfile())
    if float(spot.get_buy_price(instrument_id)) < get_five_average(instrument_id):
        system_logfile.write_logfile("downFIVE:TRUE")
        return True
    else:
        system_logfile.write_logfile("downFIVE:FALSE")
        return False

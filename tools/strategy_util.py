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


def top_fail_buy():
    logfile = Logfile(get_system_logfile())
    processedKxian = get_processed_klines(KLEN)
    x = processedKxian[-3]
    y = processedKxian[-2]
    z = processedKxian[-1]
    if top_pattern_fail(x, y, z) is True:
        logfile.write_logfile("dingfenxingFailBUY:TRUE")
        return True
    else:
        logfile.write_logfile("dingfenxingFailBUY:FALSE")
        return False


# 亏损3%止损
def stop_loss_trigger(price, instrument_id):
    system_logfile = Logfile(get_system_logfile())
    # TODO change the if condition
    if system_logfile is True: # TODO change
        system_logfile.write_logfile("3%ZhiSun:TRUE")
        return True
    else:
        system_logfile.write_logfile("3%ZhiSun:FALSE")
        return False


# 5day average
def get_five_average(instrument_id):
    sumvalue = 0.0
    spot = Spot()
    for i in range(5):
        sumvalue = sumvalue + \
                   float(spot.get_kline(instrument_id, get_previous_utc(10),
                                        get_utc_timestamp(), 864000)[-1-i].close)
    return sumvalue / 5


# 5rixian zhisahng
def is_up_five(instrument_id):
    spot = Spot()
    system_logfile = Logfile(get_system_logfile())
    if float(spot.get_kline(instrument_id, get_previous_utc(10),
                get_utc_timestamp(), 864000)[-1].close) > get_five_average(instrument_id):
        system_logfile.write_logfile("upFIVE:TRUE")
        return True
    else:
        system_logfile.write_logfile("upFIVE:FALSE")
        return False


# 5rixian zhixia
def is_down_five(instrument_id):
    spot = Spot()
    system_logfile = Logfile(get_system_logfile())
    if float(spot.get_kline(instrument_id, get_previous_utc(10),
                get_utc_timestamp(), 864000)[-1].close) < get_five_average(instrument_id):
        system_logfile.write_logfile("downFIVE:TRUE")
        return True
    else:
        system_logfile.write_logfile("downFIVE:FALSE")
        return False

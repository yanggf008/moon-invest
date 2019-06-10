# coding: utf8

from tools.get_logfile_name import *
from tools.logfile import Logfile
from tools.spot import Spot
from tools.time_util import get_previous_utc, get_utc_timestamp


def is_bottom_pattern(x, y, z):
    """
    Check whether this three klines form a bottom pattern
    :param x: the first kline
    :param y: the second kline
    :param z: the third kline
    :return: True or False for bottom pattern
    """
    if(x.period == y.period and y.period == z.period and x.high > y.high
       and x.low > y.low and y.high < z.high and y.low < z.low):
        return True
    else:
        return False


def bottom_pattern_fail(x, y, z):
    """
    Check whether this three klines fail to form a bottom pattern
    :param x: the first kline
    :param y: the second kline
    :param z: the third kline
    :return: True or False for failing bottom pattern
    """
    if(x.period == y.period and y.period == z.period and x.high > y.high
       and x.low > y.low and y.high < z.high and y.low >= z.low):
        return True
    else:
        return False


def is_top_pattern(x, y, z):
    """
    Check whether this three klines form a top pattern
    :param x: the first kline
    :param y: the second kline
    :param z: the third kline
    :return: True or False for top pattern
    """
    if(x.period == y.period and y.period == z.period and x.high < y.high
       and x.low < y.low and y.high > z.high and y.low > z.low):
        return True
    else:
        return False


def top_pattern_fail(x, y, z):
    """
    Check whether this three klines fails to form a top pattern
    :param x: the first kline
    :param y: the second kline
    :param z: the third kline
    :return: True or False for failing a top pattern
    """
    if(x.period == y.period and y.period == z.period and x.high < y.high
       and x.low < y.low and y.high <= z.high and y.low > z.low):
        return True
    else:
        return False


def get_high_max(klines):
    """
    Get the highest kline from the list of klines
    :param klines: the list of klines
    :return: the highest kline
    """
    x = klines[0]
    for item in klines:
        if item.high > x.high:
            x = item
    return x


def get_low_min(klines):
    """
    Get the lowest kline from the list of klines
    :param klines: the list of klines
    :return: the lowest kline
    """
    x = klines[0]
    for item in klines:
        if item.low < x.low:
            x = item
    return x


def up_or_down(klines):
    """
    Judge the kline list type: up or down
    :param klines: the list of klines
    :return: "up", "pure up" or "down" string
    """
    high_kline = get_high_max(klines)
    high_position = klines.index(high_kline)
    lens = len(klines)
    base_logfile = Logfile(get_base_logfile())
    # one high k contain many ks scope
    if klines[high_position].low <= get_low_min(klines[high_position:]).low:
        base_logfile.write_logfile("FENXING:pure up")
        return "pure up"
    if lens - high_position < 2:
        base_logfile.write_logfile("FENXING:up")
        return "up"
    else:
        base_logfile.write_logfile("FENXING:down")
        return "down"


def contain_include(start, klines):
    """
    Whether part of the klines(from start to end) contain including relationship
    :param start: the start of the kline list
    :param klines: the list of klines
    :return: True or false for contain including relationship
    """
    for i in range(start, len(klines) - 1):
        if (klines[i].high >= klines[i+1].high and klines[i].low <= klines[i+1].low) or \
            (klines[i].high <= klines[i+1].high and klines[i].low >= klines[i+1].low):
            return True
    return False


# chuli contains relationship  if len < 3: no process
def process_include(klines):
    """
    This function processes the including klines
    :param klines: the original klines
    :return: the processed klines
    """
    up_down_sign = up_or_down(klines)
    # start process contain relation. back contain process
    start = 0
    base_logfile = Logfile(get_base_logfile())
    while contain_include(start, klines) and start < len(klines) - 1:
        base_logfile.write_logfile("CONTAIN RELATION, POSITION:" + str(start))
        if len(klines) <= 3:
            base_logfile.write_logfile("FENXING LENGTH < 3 :BREAK")
            break
        if up_down_sign == "up" or up_down_sign == "pure up":
            for i in range(start, len(klines) - 1):
                if (klines[i].high >= klines[i + 1].high and klines[i].low <= klines[i + 1].low) or \
                        (klines[i].high <= klines[i + 1].high and klines[i].low >= klines[i + 1].low):
                    klines[i + 1].open = klines[i].open
                    if klines[i].high >= klines[i + 1].high:
                        klines[i + 1].high = klines[i].high
                    else:
                        klines[i].high = klines[i + 1].high
                    if klines[i].low >= klines[i + 1].low:
                        klines[i + 1].low = klines[i].low
                    else:
                        klines[i].low = klines[i + 1].low
                    base_logfile.write_logfile("DELUP:" + str(i))
                    del klines[i]
                    start = i
                    break
        elif up_down_sign == "down":
            for i in range(start, len(klines) - 1):
                if (klines[i].high >= klines[i + 1].high and klines[i].low <= klines[i + 1].low) or \
                        (klines[i].high <= klines[i + 1].high and klines[i].low >= klines[i + 1].low):
                    klines[i + 1].open = klines[i].open
                    if klines[i].high >= klines[i + 1].high:
                        klines[i].high = klines[i + 1].high
                    else:
                        klines[i + 1].high = klines[i].high
                    if klines[i].low >= klines[i + 1].low:
                        klines[i].low = klines[i + 1].low
                    else:
                        klines[i + 1].low = klines[i].low
                    del klines[i]
                    start = i
                    base_logfile.write_logfile("DELDOWN:" + str(i))
                    break
    return klines


def get_processed_klines(len, instrument_id, granularity):
    """
    This function return the processed including klines from the last (len) klines
    :param len: the last (len) klines
    :param instrument_id: the instrument name
    :return: the processed klines
    """
    spot = Spot()
    base_logfile = Logfile(get_base_logfile())

    kliness = spot.get_kline(instrument_id, get_previous_utc(5), get_utc_timestamp(), granularity)[-len:]
    kliness.reverse()
    processed_klines = process_include(kliness)
    base_logfile.write_logfile("GET including processed klines SUCCESS")
    return processed_klines


def is_hundred_today(instrument_id):
    """
    This function to determine whether kline today is the highest within 100 days
    :param instrument_id: the instrument name
    :return: True or False of being hundred top
    """
    spot = Spot()
    klines = spot.get_kline(instrument_id, get_previous_utc(100),
                            get_utc_timestamp(), 86400)
    top_hundred = 0
    for kline in klines:
        if top_hundred < float(kline.high):
            top_hundred = float(kline.high)
    previous_top = 0
    for kline in klines[1:]:
        if previous_top < float(kline.high):
            previous_top = float(kline.high)
    if top_hundred == float(klines[0].high) and previous_top != float(klines[1].high):
        return True
    else:
        return False




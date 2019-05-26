# coding: utf8

from tools.get_logfile_name import *
from tools.logfile import Logfile
from tools.spot import Spot
from symbol_properties import *
from tools.time_util import get_previous_utc, get_utc_timestamp


def is_bottom_pattern(x, y, z):
    if(x.period == y.period and y.period == z.period and x.high > y.high
       and x.low > y.low and y.high < z.high and y.low < z.low):
        return True
    else:
        return False


def bottom_pattern_fail(x, y, z):
    if(x.period == y.period and y.period == z.period and x.high > y.high
       and x.low > y.low and y.high < z.high and y.low >= z.low):
        return True
    else:
        return False


def is_top_pattern(x, y, z):
    if(x.period == y.period and y.period == z.period and x.high < y.high
       and x.low < y.low and y.high > z.high and y.low > z.low):
        return True
    else:
        return False


def top_pattern_fail(x, y, z):
    if(x.period == y.period and y.period == z.period and x.high < y.high
       and x.low < y.low and y.high <= z.high and y.low > z.low):
        return True
    else:
        return False


def get_high_max(klines):
    x = klines[0]
    for item in klines:
        if item.high > x.high:
            x = item
    return x


def get_low_min(klines):
    x = klines[0]
    for item in klines:
        if item.low < x.low:
            x = item
    return x


def up_or_down(klines):
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
    for i in range(start, len(klines) - 1):
        if (klines[i].high >= klines[i+1].high and klines[i].low <= klines[i+1].low) or \
            (klines[i].high <= klines[i+1].high and klines[i].low >= klines[i+1].low):
            return True
    return False


# chuli contains relationship  if len < 3: no process
def process_include(klines):
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


def get_processed_klines(len):
    kliness = []
    spot = Spot()
    base_logfile = Logfile(get_base_logfile())
    for i in range(len):
        kliness.append(spot.get_kline(SYMBOL, get_previous_utc(5),
                                      get_utc_timestamp(), TYPE))
    kliness.reverse()
    ridklines = process_include(kliness)
    base_logfile.write_logfile("GET including processed klines SUCCESS")
    return ridklines


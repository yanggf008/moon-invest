# coding:utf8
# !/usr/bin/python

import requests
import json
from tools.kline import Kline
import time
from tools.get_logfile_name import get_base_logfile
from tools.logfile import Logfile


class PriceUtil:
    # get the price of the commodity

    def __init__(self, symbol):
        self.symbol = symbol
        self.pre_url = "https://www.okex.com/api/v1/ticker.do?symbol="
        self.pre_k_url = "https://www.okex.com/api/v1/kline.do?symbol="

    def get_current_buy_price(self):
        html = requests.get(self.pre_url + self.symbol)
        json_str = json.loads(html.content)
        price = json_str["ticker"]["sell"]
        return float(price)

    def get_current_sell_price(self):
        html = requests.get(self.pre_url + self.symbol)
        json_str = json.loads(html.content)
        price = json_str["ticker"]["buy"]
        return float(price)

    # 获得kxian信息 sequence: -1 最后一个kxian信息
    def get_kline_info(self, k_type, sequence):
        html = requests.get(self.pre_k_url
                            + self.symbol + "&type=" + k_type)
        json_str = json.loads(html.content)
        print(json_str)
        high = json_str[sequence][2]
        low = json_str[sequence][3]
        k_open = json_str[sequence][1]
        close = json_str[sequence][4]
        time_value = json_str[sequence][0]
        kline = Kline(k_type, high, low, k_open, close, time_value)
        logfile = Logfile(get_base_logfile())
        logfile.write_logfile(str(kline))
        time.sleep(0.5)
        return kline


if __name__ == "__main__":
    btc_price_util = PriceUtil("btc_usdt")
    print(btc_price_util.get_current_buy_price())
    print(btc_price_util.get_current_buy_price())
    print(btc_price_util.get_kline_info("15min", -1))

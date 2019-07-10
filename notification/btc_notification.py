# coding: utf8
from tools.email_service import *
from tools.spot import *
from tools.kline_util import *
from tools.time_util import *
import time

spot = Spot()


def notify_fifteen_bottom():
    processed_klines = get_processed_klines(10, "BTC_USDT", 900)
    if is_bottom_pattern(processed_klines[-3], processed_klines[-2], processed_klines[-1]):
        print("bottom pattern")
        Email.send("15min", "bottom pattern")


def notify_exceed_price(price):
    current_price = spot.get_buy_price("BTC_USDT")
    if current_price > float(price):
        print("current price is higher than " + str(price))
        Email.send("current price > " + str(price), "current price is " + str(current_price))

# TODO: implement notify top pattern


if __name__ == "__main__":
    # Email.send("15min", "it is a bottom pattern")
    while True:
        notify_fifteen_bottom()
        notify_exceed_price(13148.5)
        time.sleep(5)

#coding: utf8
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

if __name__=="__main__":
	Email.send("15min","it is a bottom pattern")
	while True:
		notify_fifteen_bottom()
		time.sleep(5)
	
	

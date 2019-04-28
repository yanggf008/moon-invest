# coding: utf8
from tools.md5 import Md5tools
from user_properties import *
from symbol_properties import *
from tools.price_util import *
from tools.logfile import *
from tools.get_logfile_name import get_action_logfile

# action actually proceed functions


def getFundsList():
    dataMap = {"api_key": APIKEY, "secret_key": SECRETKEY}
    data = {"api_key": APIKEY, "secret_key": SECRETKEY, "sign": get_md5_value(dataMap)}
    html = requests.post("https://www.okex.com/api/v1/userinfo.do", data)
    jsonStr = json.loads(html.content)
    # return sorted(jsonStr["info"]["funds"]["free"].items(), lambda e:e[1], False)
    fundMap = jsonStr["info"]["funds"]["free"]
    # return sorted(fundMap.items(), key=lambda e: e[1], reverse=True)
    return fundMap


def logHotUsdt():
    dataMap = {"api_key": APIKEY, "secret_key": SECRETKEY}
    data = {"api_key": APIKEY, "secret_key": SECRETKEY, "sign": Md5tools.get_sign_value(dataMap)}
    html = requests.post("https://www.okex.com/api/v1/userinfo.do", data)
    jsonStr = json.loads(html.content)
    hot_value = jsonStr["info"]["funds"]["free"]["hot"]
    usdt_value = jsonStr["info"]["funds"]["free"]["usdt"]
    action_log = Logfile(get_action_logfile())
    action_log.write_logfile("SUMMARY>>HOT:" + str(hot_value) + ", USDT:" + str(usdt_value))


# ticker's bid information(buy price and amount)
def ticker_bid():
    dataMap = {"api_key": APIKEY, "secret_key": SECRETKEY}
    data = {"api_key": APIKEY, "secret_key": SECRETKEY, "sign": Md5tools.get_sign_value(dataMap), "symbol": SYMBOL}
    html = requests.get("https://www.okex.com/api/v1/depth.do", data)
    jsonStr = json.loads(html.content)
    tickerMap = jsonStr['bids'][0]
    return tickerMap


# ticker's ask information(sell price and amount)
def ticker_ask():
    dataMap = {"api_key": APIKEY, "secret_key": SECRETKEY}
    data = {"api_key": APIKEY, "secret_key": SECRETKEY, "sign": Md5tools.get_sign_value(dataMap), "symbol": SYMBOL}
    html = requests.get("https://www.okex.com/api/v1/depth.do", data)
    jsonStr = json.loads(html.content)
    tickerMap = jsonStr['asks'][-1]
    return tickerMap


def trade_buy():
    dataMap = {"api_key": APIKEY, "symbol": SYMBOL, "type": "buy",
             "price": float(ticker_ask()[0]), "amount": float(getCanBuyAmount())}
    data = {"amount": float(getCanBuyAmount()), "api_key": APIKEY, "price": float(ticker_ask()[0]), "symbol": SYMBOL, "type": "buy",
              "sign": Md5tools.get_full_sign_value(dataMap)}
    html = requests.post("https://www.okex.com/api/v1/trade.do", data)
    jsonStr = json.loads(html.content)
    tickerMap = jsonStr
    return tickerMap


def trade_sell():
    dataMap = {"api_key": APIKEY, "symbol": SYMBOL, "type": "sell",
             "price": float(ticker_bid()[0]), "amount": float(getCanSellAmount())}
    data = {"amount": float(getCanSellAmount()), "api_key": APIKEY, "price": float(ticker_bid()[0]), "symbol": SYMBOL, "type": "sell",
              "sign": Md5tools.get_full_sign_value(dataMap)}
    html = requests.post("https://www.okex.com/api/v1/trade.do", data)
    jsonStr = json.loads(html.content)
    tickerMap = jsonStr
    return tickerMap


def get_order_info():
    dataMap = {"api_key": APIKEY, "symbol": SYMBOL, "order_id": -1}
    data = {"api_key": APIKEY, "symbol": SYMBOL, "order_id": -1, "sign": Md5tools.get_full_sign_value(dataMap)}
    html = requests.post("https://www.okex.com/api/v1/order_info.do", data)
    jsonStr = json.loads(html.content)
    tickerMap = jsonStr
    return tickerMap


def get_order_id_list():
    dataMap = {"api_key": APIKEY, "symbol": SYMBOL, "order_id": -1}
    data = {"api_key": APIKEY, "symbol": SYMBOL, "order_id": -1, "sign": Md5tools.get_full_sign_value(dataMap)}
    html = requests.post("https://www.okex.com/api/v1/order_info.do", data)
    jsonStr = json.loads(html.content)
    tickerMap = jsonStr['orders']
    order_id_list = []
    for item in tickerMap:
        order_id_list.append(item['order_id'])
    return order_id_list


def cancel_all_order():
    order_id_list = get_order_id_list()
    for id in order_id_list:
        dataMap = {"api_key": APIKEY, "symbol": SYMBOL, "order_id": id}
        data = {"api_key": APIKEY, "symbol": SYMBOL, "order_id": id, "sign": Md5tools.get_full_sign_value(dataMap)}
        html = requests.post("https://www.okex.com/api/v1/cancel_order.do", data)
        action_logfile = Logfile(get_action_logfile())
        action_logfile.write_logfile("ORDER CANCELLED, ORDER_ID INFO:" + html.content)
        time.sleep(1)


def getCanSellAmount():
    buytype = SYMBOL.split("_")[0]
    if float(getFundsList().get(buytype)) > 0.01:
        return float(getFundsList().get(buytype))
    else:
        return 0.0


def getCanBuyAmount():
    selltype = SYMBOL.split("_")[1]
    if float(getFundsList().get(selltype)) / getCurrentSellPrice(SYMBOL) > 0.01:
        return float(getFundsList().get(selltype)) / getCurrentSellPrice(SYMBOL) * 0.95
    else:
        return 0.0


def trade_buy_three_times():
    cancel_all_order()
    time.sleep(2)
    sign = trade_buy()
    num = 0
    while str(sign).find('error_code') != -1:
        writeLogFile(getActionLogFile(), "TRADE_BUY_HOT INFO:" + str(sign))
        sign = trade_buy()
        time.sleep(1)
        num += 1
        if num > 2:
            break


def trade_sell_three_times():
    cancel_all_order()
    time.sleep(2)
    sign = trade_sell()
    num = 0
    while str(sign).find('error_code') != -1:
        writeLogFile(getActionLogFile(), "TRADE_SELL_HOT INFO:" + str(sign))
        sign = trade_sell()
        time.sleep(1)
        num += 1
        if num > 2:
            break

if __name__ == "__main__":
    logHotUsdt()
    # trade_buy_three_times()
    # print trade_sell()
    # print getFundsList()
    # print get_order_info()
    # print get_order_id_list()
    # cancel_all_order()
    # print getCanSellAmount(), getCanBuyAmount()
    # print ticker_bid(), ticker_ask()
    # print getCanBuyAmount()
# coding: utf8
from tools.md5 import Md5tools
from user_properties import *
from symbol_properties import *
from tools.price import *
from tools.logfile import *
from tools.get_logfile_name import get_action_logfile

# action actually proceed functions


def get_fund_list():
    data_map = {"api_key": APIKEY, "secret_key": SECRETKEY}
    data = {"api_key": APIKEY, "secret_key": SECRETKEY, "sign": Md5tools.get_sign_value(data_map)}
    html = requests.post("https://www.okex.com/api/v1/userinfo.do", data)
    funds_json = json.loads(html.content)
    # return sorted(jsonStr["info"]["funds"]["free"].items(), lambda e:e[1], False)
    funds_map = funds_json["info"]["funds"]["free"]
    # return sorted(fundMap.items(), key=lambda e: e[1], reverse=True)
    return funds_map


def log_hot_usdt():
    data_map = {"api_key": APIKEY, "secret_key": SECRETKEY}
    data = {"api_key": APIKEY, "secret_key": SECRETKEY, "sign": Md5tools.get_full_sign_value(data_map)}
    html = requests.post("https://www.okex.com/api/v1/userinfo.do", data)
    hot_json = json.loads(html.content)
    hot_value = hot_json["info"]["funds"]["free"]["hot"]
    usdt_value = hot_json["info"]["funds"]["free"]["usdt"]
    action_log = Logfile(get_action_logfile())
    action_log.write_logfile("SUMMARY>>HOT:" + str(hot_value) + ", USDT:" + str(usdt_value))


# ticker's bid information(buy price and amount)
def ticker_bid():
    data_map = {"api_key": APIKEY, "secret_key": SECRETKEY}
    data = {"api_key": APIKEY, "secret_key": SECRETKEY, "sign": Md5tools.get_sign_value(data_map), "symbol": SYMBOL}
    html = requests.get("https://www.okex.com/api/v1/depth.do", data)
    ticker_json = json.loads(html.content)
    ticker_map = ticker_json['bids'][0]
    return ticker_map


# ticker's ask information(sell price and amount)
def ticker_ask():
    data_map = {"api_key": APIKEY, "secret_key": SECRETKEY}
    data = {"api_key": APIKEY, "secret_key": SECRETKEY, "sign": Md5tools.get_sign_value(data_map), "symbol": SYMBOL}
    html = requests.get("https://www.okex.com/api/v1/depth.do", data)
    ask_json = json.loads(html.content)
    ticker_map = ask_json['asks'][-1]
    return ticker_map


def trade_buy():
    data_map = {"api_key": APIKEY, "symbol": SYMBOL, "type": "buy",
             "price": float(ticker_ask()[0]), "amount": float(getCanBuyAmount())}
    data = {"amount": float(getCanBuyAmount()), "api_key": APIKEY, "price": float(ticker_ask()[0]), "symbol": SYMBOL, "type": "buy",
              "sign": Md5tools.get_full_sign_value(data_map)}
    html = requests.post("https://www.okex.com/api/v1/trade.do", data)
    trade_json = json.loads(html.content)
    ticker_map = trade_json
    return ticker_map


def trade_sell():
    data_map = {"api_key": APIKEY, "symbol": SYMBOL, "type": "sell",
             "price": float(ticker_bid()[0]), "amount": float(getCanSellAmount())}
    data = {"amount": float(getCanSellAmount()), "api_key": APIKEY, "price": float(ticker_bid()[0]), "symbol": SYMBOL, "type": "sell",
              "sign": Md5tools.get_full_sign_value(data_map)}
    html = requests.post("https://www.okex.com/api/v1/trade.do", data)
    sell_json = json.loads(html.content)
    ticker_map = sell_json
    return ticker_map


def get_order_info():
    data_map = {"api_key": APIKEY, "symbol": SYMBOL, "order_id": -1}
    data = {"api_key": APIKEY, "symbol": SYMBOL, "order_id": -1, "sign": Md5tools.get_full_sign_value(data_map)}
    html = requests.post("https://www.okex.com/api/v1/order_info.do", data)
    order_json = json.loads(html.content)
    order_info_map = order_json
    return order_info_map


def get_order_id_list():
    data_map = {"api_key": APIKEY, "symbol": SYMBOL, "order_id": -1}
    data = {"api_key": APIKEY, "symbol": SYMBOL, "order_id": -1, "sign": Md5tools.get_full_sign_value(data_map)}
    html = requests.post("https://www.okex.com/api/v1/order_info.do", data)
    order_json = json.loads(html.content)
    order_map = order_json['orders']
    order_id_list = []
    for item in order_map:
        order_id_list.append(item['order_id'])
    return order_id_list


def cancel_all_order():
    order_id_list = get_order_id_list()
    for id in order_id_list:
        data_map = {"api_key": APIKEY, "symbol": SYMBOL, "order_id": id}
        data = {"api_key": APIKEY, "symbol": SYMBOL, "order_id": id, "sign": Md5tools.get_full_sign_value(data_map)}
        html = requests.post("https://www.okex.com/api/v1/cancel_order.do", data)
        action_logfile = Logfile(get_action_logfile())
        action_logfile.write_logfile("ORDER CANCELLED, ORDER_ID INFO:" + html.content)
        time.sleep(1)


def get_can_sell_amout():
    buy_type = SYMBOL.split("_")[0]
    if float(get_fund_list().get(buy_type)) > 0.01:
        return float(get_fund_list().get(buy_type))
    else:
        return 0.0


def get_can_buy_amount():
    sell_type = SYMBOL.split("_")[1]
    symbol_price = Price(SYMBOL)
    if float(get_fund_list().get(sell_type)) / symbol_price.get_current_sell_price() > 0.01:
        return float(get_fund_list().get(sell_type)) / symbol_price.get_current_sell_price() * 0.95
    else:
        return 0.0


def trade_buy_three_times():
    cancel_all_order()
    time.sleep(2)
    sign = trade_buy()
    num = 0
    action_logfile = Logfile(get_action_logfile())
    while str(sign).find('error_code') != -1:
        action_logfile.write_logfile("TRADE_BUY_HOT INFO:" + str(sign))
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
    action_logfile = Logfile(get_action_logfile())
    while str(sign).find('error_code') != -1:
        action_logfile.write_logfile("TRADE_SELL_HOT INFO:" + str(sign))
        sign = trade_sell()
        time.sleep(1)
        num += 1
        if num > 2:
            break


if __name__ == "__main__":
    log_hot_usdt()
    # trade_buy_three_times()
    # print trade_sell()
    # print getFundsList()
    # print get_order_info()
    # print get_order_id_list()
    # cancel_all_order()
    # print getCanSellAmount(), getCanBuyAmount()
    # print ticker_bid(), ticker_ask()
    # print getCanBuyAmount()
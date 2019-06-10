# coding: utf8
from user_properties import *
from tools.price import *
from tools.time_util import *
import hashlib
import base64
import hmac
from tools.consts import *
from tools.okex_utils import get_header, sign, pre_hash


def get_public_currencies():
    """
    All REST requests must contain the following headers:
    OK-ACCESS-KEY The api key as a String.
    OK-ACCESS-SIGN The base64-encoded signature (see Signing a Message).
    OK-ACCESS-TIMESTAMP A timestamp for your request.
    OK-ACCESS-PASSPHRASE The passphrase you specified when creating the API key.
    All request bodies should have content type application/json and be valid JSON.
    :return: a list contains all the names of currencies
    """
    timestamp = get_utc_timestamp()
    host = "https://www.okex.com/api/account/v3/currencies"
    content = timestamp + "GET" + "/api/account/v3/currencies"
    h = hmac.new(bytes(SECRETKEY, "utf8"), bytes(content, "utf8"), hashlib.sha256).digest()
    signature = base64.b64encode(h)
    headers = {
        "OK-ACCESS-KEY": APIKEY,
        "OK-ACCESS-SIGN": signature,
        "CONTENT-TYPE": "application/json",
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": PASSPHRASE
    }
    currencies_response = requests.get(host, headers=headers)
    content = currencies_response.content
    str_content = content.decode('utf8')
    json_content = json.loads(str_content)
    currencies_list = []
    for item in json_content:
        currencies_list.append(item["currency"])
    return currencies_list


def get_spot_info():
    request_path = SPOT_ACCOUNT_INFO
    timestamp = get_utc_timestamp()
    hash_content = pre_hash(timestamp, GET, request_path, "")
    header = get_header(timestamp, sign(hash_content))
    response = requests.get(API_URL+request_path, headers=header)
    return response.json()


def get_currency_amount(currency):
    request_path = SPOT_ACCOUNT_INFO
    timestamp = get_utc_timestamp()
    hash_content = pre_hash(timestamp, GET, request_path, "")
    header = get_header(timestamp, sign(hash_content))
    response = requests.get(API_URL+request_path, headers=header)
    amount = 0
    for item in response.json():
        if item['currency'] == str.upper(currency):
            amount = item['available']
    return float(amount)




#
#
# def get_order_info():
#     data_map = {"api_key": APIKEY, "symbol": SYMBOL, "order_id": -1}
#     data = {"api_key": APIKEY, "symbol": SYMBOL, "order_id": -1, "sign": Md5tools.get_full_sign_value(data_map)}
#     html = requests.post("https://www.okex.com/api/v1/order_info.do", data)
#     order_json = json.loads(html.content)
#     order_info_map = order_json
#     return order_info_map
#
#
# def get_order_id_list():
#     data_map = {"api_key": APIKEY, "symbol": SYMBOL, "order_id": -1}
#     data = {"api_key": APIKEY, "symbol": SYMBOL, "order_id": -1, "sign": Md5tools.get_full_sign_value(data_map)}
#     html = requests.post("https://www.okex.com/api/v1/order_info.do", data)
#     order_json = json.loads(html.content)
#     order_map = order_json['orders']
#     order_id_list = []
#     for item in order_map:
#         order_id_list.append(item['order_id'])
#     return order_id_list
#
#
# def cancel_all_order():
#     order_id_list = get_order_id_list()
#     for id in order_id_list:
#         data_map = {"api_key": APIKEY, "symbol": SYMBOL, "order_id": id}
#         data = {"api_key": APIKEY, "symbol": SYMBOL, "order_id": id, "sign": Md5tools.get_full_sign_value(data_map)}
#         html = requests.post("https://www.okex.com/api/v1/cancel_order.do", data)
#         action_logfile = Logfile(get_action_logfile())
#         action_logfile.write_logfile("ORDER CANCELLED, ORDER_ID INFO:" + html.content)
#         time.sleep(1)


# def get_can_sell_amout():
#     buy_type = SYMBOL.split("_")[0]
#     if float(get_fund_list().get(buy_type)) > 0.01:
#         return float(get_fund_list().get(buy_type))
#     else:
#         return 0.0
#
#
# def get_can_buy_amount():
#     sell_type = SYMBOL.split("_")[1]
#     symbol_price = Price(SYMBOL)
#     if float(get_fund_list().get(sell_type)) / symbol_price.get_current_sell_price() > 0.01:
#         return float(get_fund_list().get(sell_type)) / symbol_price.get_current_sell_price() * 0.95
#     else:
#         return 0.0
#
#
# def trade_buy_three_times():
#     cancel_all_order()
#     time.sleep(2)
#     sign = trade_buy()
#     num = 0
#     action_logfile = Logfile(get_action_logfile())
#     while str(sign).find('error_code') != -1:
#         action_logfile.write_logfile("TRADE_BUY_HOT INFO:" + str(sign))
#         sign = trade_buy()
#         time.sleep(1)
#         num += 1
#         if num > 2:
#             break
#
#
# def trade_sell_three_times():
#     cancel_all_order()
#     time.sleep(2)
#     sign = trade_sell()
#     num = 0
#     action_logfile = Logfile(get_action_logfile())
#     while str(sign).find('error_code') != -1:
#         action_logfile.write_logfile("TRADE_SELL_HOT INFO:" + str(sign))
#         sign = trade_sell()
#         time.sleep(1)
#         num += 1
#         if num > 2:
#             break

if __name__ == "__main__":
    print(get_public_currencies())
    print(get_spot_info())
    print(get_currency_amount("yee"))

# coding: utf8
from tools.client import Client
from tools.consts import *


class Spot(Client):
    """
    This class stands for the spot account
    """
    def __init__(self, use_server_time=False):
        """
        the constructor of Spot class derived from Client
        :param use_server_time:  whether use server side timestamp
        """
        Client.__init__(self, use_server_time)

    def get_currency_amount(self, currency):
        """
        get the currency amount in your spot account
        :param currency: (string)the name of the currency you want to query
        :return : (float)the amount of the currency
        """
        spot_json = self._request_without_params(GET, SPOT_ACCOUNT_INFO)
        amount = 0
        for item in spot_json:
            if item['currency'] == str.upper(currency):
                amount = item['available']
        return float(amount)

    def get_usdt_amount(self):
        """
        get usdt amount in your spot account
        :return : (float)the amount of usdt
        """
        spot_json = self._request_without_params(GET, SPOT_ACCOUNT_INFO)
        amount = 0
        for item in spot_json:
            if item['currency'] == str.upper("usdt"):
                amount = item['available']
        return float(amount)

    def get_sell_list(self, instrument_id):
        """
        get the sell details of the currency
        :param instrument_id: the name of the currency
        :return: the sell price list of the currency({[price, amount, num],})
        """
        return self.get_depth(instrument_id)['asks']

    def get_sell_price(self, instrument_id):
        """
        get the sell price of the currency
        :param instrument_id: the name of the currency
        :return: the sell first price of the currency(float)
        """
        return float(self.get_depth(instrument_id)['asks'][0][0])

    def get_depth(self, instrument_id, size='', depth=''):
        """
        This function get the depth of the symbol(instrument_id)
        :param instrument_id: symbol pair "yee-usdt"
        :param size: the size of the depth list
        :param depth: aggregation is the formation a certain price range into a cluster
        :return: the json result of the depth list
        """
        params = {}
        if size:
            params['size'] = str(size)
        if depth:
            params['depth'] = depth
        return self._request(GET, SPOT_DEPTH + str(instrument_id) + '/book', params)

    def get_buy_list(self, instrument_id):
        """
        get the buy details of the currency
        :param instrument_id: the name of the currency
        :return: the buy price list of the currency({[price, amount, num],})
        """
        return self.get_depth(instrument_id)['bids']

    def get_buy_price(self, instrument_id):
        """
        get the buy price of the currency
        :param instrument_id: the name of the currency
        :return: the buy price of the currency(float)
        """
        return self.get_depth(instrument_id)['bids'][0][0]

    def get_buy_amount(self, instrument_id):
        """
        Get the amount of the currency we can buy
        :param instrument_id: the currency name
        :return: the amount we can buy for the currency(float)
        """
        usdt = self.get_usdt_amount()
        return float(usdt/self.get_sell_price(instrument_id))

    def take_order(self, otype, side, instrument_id, size, margin_trading=1, client_oid='', price='', funds='',
                   order_type=''):
        """
        This function is to place an order in spot account
        :param otype: order type (limit, market)
        :param side: order direction (buy, sell)
        :param instrument_id: the name of crypto currency
        :param size: quantity
        :param margin_trading: order type (the request value is 1)
        :param client_oid: the order id customised by user
        :param price: the price of the order
        :param funds:
        :param order_type: Fill in number for parameter, 0: normal limit order, 1: post only, 2: fill or kill
                        3: immediate or cancel
        :return: None
        """
        params = {'type': otype, 'side': side, 'instrument_id': instrument_id, 'size': size, 'client_oid': client_oid,
                  'price': price, 'funds': funds, 'margin_trading': margin_trading, 'order_type': order_type}
        return self._request(POST, SPOT_ORDER, params)

    def get_currency_list(self):
        """
        Get the currency list
        :return: the currency list
        """
        currency_info = self._request_without_params(GET, CURRENCIES_INFO)
        currency_list = []
        for item in currency_info:
            currency_list.append(item['currency'])
        return currency_list

    def get_instrument_list(self):
        """
        Get instrument id list
        :return: a instrument list (trade pair)
        """
        instrument_info = self._request_without_params(GET, SPOT_COIN_INFO)
        instrument_list = []
        for instrument in instrument_info:
            instrument_list.append(instrument["instrument_id"])
        return instrument_list

    def get_instrument_price(self):
        """
        Get instrument map including the price
        :return: (map) contains instruments' id and price
        """
        instrument_info = self._request_without_params(GET, SPOT_TICKER)
        instrument_map = {}
        for instrument in instrument_info:
            instrument_map[instrument["instrument_id"]] = float(instrument["best_bid"])
        return instrument_map

    def get_top_instrument(self, n):
        """
        Get top n instrument based on the usdt price
        :param n: n >= 1
        :return: the top n instrument list
        """
        instrument_map = self.get_instrument_price()
        filtered_keys = list(filter(lambda x: str(x).endswith("USDT"), instrument_map.keys()))
        filtered_list = [(k, instrument_map[k]) for k in filtered_keys]
        return sorted(filtered_list, key=lambda d: d[1], reverse=True)[:n]


if __name__ == "__main__":
    spot = Spot()
    # print(spot.get_currency_amount("yee"))
    # print(spot.get_depth("btc-usdt"))
    # print(spot.get_depth("yee-usdt", 1))
    # print(spot.get_depth("yee-usdt", 1, "0.001"))
    # print(spot.get_depth("yee-usdt", 10, "0.99"))
    # print(spot.get_sell_list("yee-usdt"))
    # print(spot.get_usdt_amount())
    # print(spot.get_sell_price('r-usdt'))
    # print(spot.get_buy_price('btc-usdt'))
    # print(spot.get_buy_amount('yee-usdt'))
    print(spot.get_instrument_price())
    print(spot.get_top_instrument(5))

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

    def depth_sell_list(self, instrument_id):
        """
        get the sell details of the currency
        :param instrument_id: the name of the currency
        :return: the sell price list of the currency
        """
        return self.get_depth(instrument_id)['asks']


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


if __name__ == "__main__":
    spot = Spot()
    print(spot.get_currency_amount("yee"))
    print(spot.get_depth("btc-usdt"))
    print(spot.get_depth("yee-usdt", 1))
    print(spot.get_depth("yee-usdt", 1, "0.001"))
    print(spot.get_depth("yee-usdt", 10, "0.99"))
    print(spot.depth_sell_list("yee-usdt"))

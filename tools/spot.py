# coding: utf8
from tools.client import Client
from tools.consts import *
from tools.time_util import get_utc_timestamp


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


if __name__ == "__main__":
    spot = Spot()
    print(spot.get_currency_amount("yee"))
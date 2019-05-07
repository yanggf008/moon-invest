# coding: utf8
from tools.client import Client
from user_properties import *
from tools.consts import *
from tools.time_util import get_utc_timestamp


class Spot(Client):

    def __init__(self, use_server_time=False):
        Client.__init__(self, use_server_time)

    def get_currency_amount(self, currency):
        spot_json = self._request_without_params(GET, SPOT_ACCOUNT_INFO)
        amount = 0
        for item in spot_json:
            if item['currency'] == str.upper(currency):
                amount = item['available']
        return float(amount)


if __name__ == "__main__":
    spot = Spot()
    print(spot.get_currency_amount("yee"))
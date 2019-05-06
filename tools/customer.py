#coding: utf8

import requests
import json
from tools.consts import *
from user_properties import *
from tools.okex_utils import *
from tools.time_util import get_utc_timestamp


class Client:
    def __init__(self, use_server_time=False):
        self.APIKEY = APIKEY
        self.SECRETKEY = SECRETKEY
        self.PASSPHRASE = PASSPHRASE
        self.use_server_time = use_server_time


    def _request(self, method, request_path, params):
        if method == "GET":
            request_path = request_path + params_to_url(params)
        url = API_URL + request_path
        timestamp = get_utc_timestamp()
        if self.use_server_time is True:
            timestamp = self._get_server_timestamp()
        if method == POST:
            body = json.dumps(params)
        else:
            body = ""
        signed_value = sign(pre_hash(timestamp, method, request_path, body))
        headers = get_header(timestamp, signed_value)

        response = None



    def _get_server_timestamp(self):
        url = API_URL + SERVER_TIMESTAMP_URL
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['iso']
        else:
            return ""
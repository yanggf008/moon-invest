# coding: utf8

import requests
import json
from tools.consts import *
from tools.exceptions import *
from tools.okex_utils import *
from tools.time_util import get_utc_timestamp


class Client:
    """
    This class stands for a client account
    """
    def __init__(self, use_server_time=False):
        """
        This is the constructor of the client class
        :param use_server_time: whether use server time or not
        """
        self.APIKEY = APIKEY
        self.SECRETKEY = SECRETKEY
        self.PASSPHRASE = PASSPHRASE
        self.use_server_time = use_server_time

    def _request(self, method, request_path, params):
        """
        The basic request behavior for client account
        :param method: GET or POST or DELETE
        :param request_path: '/api/.../...' stands for a function
        :param params: request params
        :return: return the result of the request
        """
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
        if method == GET:
            response = requests.get(url, headers=headers)
        elif method == POST:
            response = requests.post(url, data=body, headers=headers)
        elif method == DELETE:
            response == requests.delete(url, headers=headers)

        if not str(response.status_code).startswith('2'):
            raise OkexRequestsException(response)
        else:
            return response.json()

    def _request_without_params(self, method, request_path):
        """
        The basic request behavior for client account without params
        :param method: GET or POST or DELETE
        :param request_path: '/api/.../...' stands for a function
        :return: return the result of the request without params
        """
        return self._request(method, request_path, {})

    @staticmethod
    def _get_server_timestamp():
        url = API_URL + SERVER_TIMESTAMP_URL
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['iso']
        else:
            return ""



# coding: utf8
import hashlib
import base64
import hmac
from user_properties import *


def sign(message):
    """
    This function used to generate the hash value
    :param message: the content should be hashed
    :return: the hash value of the content
    """
    h = hmac.new(bytes(SECRETKEY, "utf8"),
                 bytes(message, "utf8"), hashlib.sha256).digest()
    signed_value = base64.b64encode(h)
    return signed_value


def pre_hash(timestamp, method, request_path, body):
    """
    This function generate the message which should be hashed
    :param timestamp: UTC type of timestamp
    :param method: 'GET' or 'POST'
    :param request_path: '/api/.../...' stands for a certain function
    :param body: body content of the request
    :return: return the generated message
    """
    if method == "GET":
        body = ""
    hash_content = str(timestamp) + str.upper(method) +\
        str(request_path) + str(body)
    return hash_content


def get_header(timestamp, signed_value):
    """
    This function is used to generate header for okex api3 request
    :param timestamp: UTC type timestamp endwith 'Z' split by 'T'
    :param signed_value: hash value of message sha256 and base64
    :return: header dict
    """
    headers = {
        "OK-ACCESS-KEY": APIKEY,
        "OK-ACCESS-SIGN": signed_value,
        "CONTENT-TYPE": "application/json",
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": PASSPHRASE
    }
    return headers


def params_to_url(params):
    """
    This function return the url generated by params
    :param params: a parameter dict contains several params
    :return: the url generated from params
    """
    url = '?'
    for (key, value) in params.items():
        url = url + str(key) + '=' + str(value) + '&'
    return url[:-1]


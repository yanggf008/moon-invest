# coding: utf8
import hashlib
from urllib.parse import urlencode
from user_properties import SECRETKEY


class Md5tools:
    @staticmethod
    def get_sign_value(data_map):
        """ Get MD5 value of OKEX URL
        using built-in hashlib package get md5 digest of your OKEX key

        Parameters:
        :argument1 (dict)

        :return:
        int: Retuning MD5 value
        """
        data_maps = sorted(data_map.items(), key=lambda e: e[0], reverse=False)
        str_data = urlencode(data_maps)
        my_md5 = hashlib.md5()  # get a MD5 encryption object
        my_md5.update(str_data.encode("utf8"))  # get the message's MD5 digest
        my_md5_digest = my_md5.hexdigest()  # return 32 bits digest in HEX
        return my_md5_digest.upper()

    @staticmethod
    def get_full_sign_value(data_map):
        """ Get full MD5 value of OKEX URL including secret key
        using built-in hashlib package get md5 digest of your OKEX key

        Parameters:
        :argument1 (dict)

        :return:
        int: Retuning full MD5 value
        """
        data_maps = sorted(data_map.items(), key=lambda e: e[0], reverse=False)
        str_data = urlencode(data_maps)
        secret_key = "&secret_key=" + SECRETKEY
        my_md5 = hashlib.md5()  # get a MD5 encryption object
        my_md5.update((str_data+secret_key).encode("utf8"))  # get the message's MD5 digest
        my_md5_digest = my_md5.hexdigest()  # return 32 bits digest in HEX
        return my_md5_digest.upper()


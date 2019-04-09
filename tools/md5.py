# coding: utf8
import hashlib, urllib


# using built-in hashlib package get md5 digest of your OKEX key
class Md5tools:
    
    def get_sign_value(data_map):
        data_maps = sorted(data_map.items(), key=lambda e: e[0], reverse=False)
        str_data = urllib.urlencode(data_maps)
        secret_key = "&secret_key=YOUR_KEY"
        my_md5 = hashlib.md5()  # get a MD5 encryption object
        my_md5.update(str_data + secret_key)  # get the message's MD5 digest
        my_md5_digest = my_md5.hexdigest()  # return 32 bits digest in HEX
        return my_md5_digest.upper()

if __name__ == "__main__":
    dataMap = {"api_key": "YOUR_APIKEY", "secretkey": "YOUR_SECRETKEY"}
    print get_md5_value(dataMap)

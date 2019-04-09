# coding: utf8
import hashlib, urllib


# using built-in hashlib package get md5 digest of your OKEX key

def get_sign_value(dataMap):
    dataMaps = sorted(dataMap.items(), key=lambda e: e[0], reverse=False)
    str = urllib.urlencode(dataMaps)
    secret_key = "&secret_key=YOUR_KEY"
    my_md5 = hashlib.md5()  # get a MD5 encryption object
    my_md5.update(str+secret_key)  # get the message's MD5 digest
    my_md5_Digest = my_md5.hexdigest()  # return 32 bits digest in HEX
    return my_md5_Digest.upper()

if __name__ == "__main__":
    dataMap = {"api_key": "YOUR_APIKEY", "secretkey": "YOUR_SECRETKEY"}
    print get_md5_value(dataMap)

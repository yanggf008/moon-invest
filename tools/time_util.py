# coding: utf8
import time
import datetime
from datetime import timedelta


def get_timestamp():
    """
    This function is to return the value of the current timestamp
    :return: a String of timestamp
    """
    return str(time.time_ns())


def get_utc_timestamp():
    """
    This function is to return the value of the UTC format time
    This timestamp is used for okex v3 api
    :return: a string of time in UTC format
    """
    return datetime.datetime.utcnow().isoformat()[:-3] + "Z"


def get_previous_utc(n):
    """
    This function is to get the value of the n day ago time
    :return: (string) n day ago time in UTC format
    """
    ago_time = datetime.datetime.utcnow() - timedelta(days=n)
    return ago_time.isoformat()[:-3] + "Z"


def get_day():
    """
    This function is to return the value of the current date in format -%Y-%m-%d
    :return: a String of current date
    """
    return str(time.strftime("-%Y-%m-%d", time.localtime()))


def get_format_time():
    """
    This function is to return the exact time in format %Y-%m-%d %H:%M:%S
    :return: a String of current time
    """
    return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


if __name__ == "__main__":
    print(datetime.datetime.utcnow().isoformat()[:-3] + "Z")
    print(get_timestamp())
    print(get_utc_timestamp())
    print(get_previous_utc(23))

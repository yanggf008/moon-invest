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


def utc_to_timestamp(utc_time):
    utc_str = datetime.datetime.strptime(utc_time[:-5], "%Y-%m-%dT%H:%M:%S")
    return str(utc_str.timestamp())[:-2]


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


def get_future_suffix():
    today = datetime.date.today()
    friday = today + datetime.timedelta((4 - today.weekday()) % 7)
    friday_str = time.strftime("%Y%m%d", friday.timetuple())
    return str(friday_str)[2:]


if __name__ == "__main__":
    print(datetime.datetime.utcnow().isoformat()[:-3] + "Z")
    print((datetime.datetime.utcnow() - timedelta(hours=4)).isoformat())
    print(get_utc_timestamp())
    print(get_previous_utc(23))
    print(utc_to_timestamp("2019-05-22T03:25:10.482Z"))
    print(get_future_suffix())
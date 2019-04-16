# coding: utf8
import time


def get_timestamp():
    """
    This function is to return the value of the current timestamp
    :return: a String of timestamp
    """
    return str(int(time.time()))


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

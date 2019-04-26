# coding: utf8
from tools.time_util import get_day


def get_system_logfile():
    """
    This function is to return the system logfile name
    :return: a String of System logfile name
    """
    return "system" + get_day() + ".log"


def get_fifteen_logfile():
    """
    This function is to return the fifteen strategy logfile name
    :return: a String of Fifteen Strategy logfile name
    """
    return "fifteenStrategy" + get_day() + ".log"


def get_base_logfile():
    """
    This function is to return the base logfile name
    :return: a String of Base logfile name
    """
    return "baseLog" + get_day() + ".log"


def get_fund_logfile():
    """
    This function is to return the fund logfile name
    :return: a String of fund logfile name
    """
    return "fund" + get_day() + ".log"


def get_action_logfile():
    """
    This function is to return the action logfile name
    :return: a String of action logfile name
    """
    return "action" + get_day() + ".log"

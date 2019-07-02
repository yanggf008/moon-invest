# coding: utf-8

from tools.spot import *

spot = Spot()


def buyTsellK_percent(kd_pair):
    instrument_usdk = kd_pair[0]
    instrument_usdt = kd_pair[1]
    can_sell_usdk = spot.get_kd_sell_price(instrument_usdk)
    can_buy_usdt = spot.get_kd_buy_price(instrument_usdt)
    return (can_sell_usdk - can_buy_usdt) / can_buy_usdt


def buyKsellT_percent(kd_pair):
    instrument_usdk = kd_pair[0]
    instrument_usdt = kd_pair[1]
    can_sell_usdt = spot.get_kd_sell_price(instrument_usdt)
    can_buy_usdk = spot.get_kd_buy_price(instrument_usdk)
    return (can_sell_usdt - can_buy_usdk) / can_buy_usdk


def trading_amount(kd_pair):
    instrument_usdk = kd_pair[0]
    instrument_usdt = kd_pair[1]
    usdk_amount = spot.get_usdk()
    usdt_amount = spot.get_usdt()
    real_amount = 0.0
    if is_one_percent(kd_pair) == "buyKsellT":
        buy_cap = spot.get_kd_buy_price(instrument_usdk) * spot.get_kd_buy_amount(instrument_usdk)
        sell_cap = spot.get_kd_sell_price(instrument_usdt) * spot.get_kd_sell_amount(instrument_usdt)
        real_amount = min(min(buy_cap, sell_cap), usdk_amount)
    if is_one_percent(kd_pair) == "buyTsellK":
        buy_cap = spot.get_kd_buy_price(instrument_usdt) * spot.get_kd_buy_amount(instrument_usdt)
        sell_cap = spot.get_kd_sell_price(instrument_usdk) * spot.get_kd_sell_amount(instrument_usdk)
        real_amount = min(min(buy_cap, sell_cap), usdt_amount)
    return real_amount


def trading_list():
    kd_pairs = spot.get_usdkt_list()
    trading_info = []
    for pair in kd_pairs:
        trading_info.append((pair[0], pair[1], buyTsellK_percent(pair), buyKsellT_percent(pair)))
    return trading_info


def cmp(a, b):
    if a>b:
        return 1
    elif a<b:
        return -1
    else:
        return 0


if __name__ == "__main__":
    trading = trading_list()
    sorted_list = sorted(trading, key=lambda x: x[3])
    print(sorted_list)
    instrument_id = sorted_list[-1][0]
    print(instrument_id)
    # spot.take_order(side="buy", instrument_id=instrument_id, price=buy_price, size=buy_size)



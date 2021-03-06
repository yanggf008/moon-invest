from tools.client import Client
from tools.consts import *
import json


class FutureAPI(Client):

    def __init__(self, use_server_time=False):
        Client.__init__(self, use_server_time)

    # query position
    def get_position(self):
        return self._request_without_params(GET, FUTURE_POSITION)

    def get_BTC_long_avail_qty(self):
        position_json = self.get_position()
        position_list = []
        for position_item in position_json['holding'][0]:
            instrument_id = position_item['instrument_id']
            long_avail_qty = position_item['long_avail_qty']
            position_list.append((instrument_id, long_avail_qty))
        for position_item in position_list:
            if "BTC" in position_item[0]:
                return float(position_item[1])
        return 0.0

    # query specific position
    def get_specific_position(self, instrument_id):
        return self._request_without_params(GET, FUTURE_SPECIFIC_POSITION + str(instrument_id) + '/position')

    # query accounts info
    def get_accounts(self):
        return self._request_without_params(GET, FUTURE_ACCOUNTS)

    # query coin account info
    def get_coin_account(self, symbol):
        return self._request_without_params(GET, FUTURE_COIN_ACCOUNT + str(symbol))

    # query leverage
    def get_leverage(self, symbol):
        return self._request_without_params(GET, FUTURE_GET_LEVERAGE + str(symbol) + '/leverage')

    # set leverage
    def set_leverage(self, currency, leverage, instrument_id='', direction=''):
        params = {'leverage': leverage}
        if instrument_id:
            params['instrument_id'] = instrument_id
        if direction:
            params['direction'] = direction
        print(params)
        return self._request(POST, FUTURE_SET_LEVERAGE + str(currency) + '/leverage', params)

    # query ledger
    def get_ledger(self, symbol):
        return self._request_without_params(GET, FUTURE_LEDGER + str(symbol) + '/ledger')

    # delete position
    # def revoke_position(self, position_data):
    #     params = {'position_data': position_data}
    #     return self._request(DELETE, FUTURE_DELETE_POSITION, params)
    def revoke_position(self, position_data):
        params = {'position_data': position_data}
        return self._request(POST, FUTURE_DELETE_POSITION, params)

    # take order
    def take_order(self, client_oid, instrument_id, otype, price, size, match_price, leverage):
        #param size 1 means 0.01
        params = {'client_oid': client_oid, 'instrument_id': instrument_id, 'type': otype, 'price': price, 'size': size,
                  'match_price': match_price, 'leverage': leverage}
        return self._request(POST, FUTURE_ORDER, params)

    # take orders
    def take_orders(self, instrument_id, orders_data, leverage):
        params = {'instrument_id': instrument_id, 'orders_data': orders_data, 'leverage': leverage}
        return self._request(POST, FUTURE_ORDERS, params)

    # revoke order
    def revoke_order(self, instrument_id, order_id='',client_oid=''):
        if order_id:
            return self._request_without_params(POST, FUTURE_REVOKE_ORDER + str(instrument_id) + '/' + str(order_id))
        elif client_oid:
            return self._request_without_params(POST, FUTURE_REVOKE_ORDER + str(instrument_id) + '/' + str(client_oid))

    # revoke orders

    def revoke_orders(self, instrument_id, order_ids='',client_oids=''):
        if order_ids:
            params = {'order_ids': order_ids}
        elif client_oids:
            params = {'client_oids': client_oids}
        return self._request(POST, FUTURE_REVOKE_ORDERS+str(instrument_id), params)

    # query order list
    #def get_order_list(self, status, before, after, limit, instrument_id=''):
    #   params = {'status': status, 'before': before, 'after': after, 'limit': limit, 'instrument_id': instrument_id}
    #    return self._request(GET, FUTURE_ORDERS_LIST, params)

    # query order list
    def get_order_list(self, status,  instrument_id='', limit=100):
        params = {'status': status, 'instrument_id': instrument_id}
        if limit:
            params['limit'] = limit
        return self._request(GET, FUTURE_ORDERS_LIST+'/'+str(instrument_id), params)

    def get_uncomplete_order(self, instrument_id):
        order_list = self.get_order_list(status="6", instrument_id=instrument_id)
        orderID_list = []
        for order in order_list["order_info"]:
            orderID_list.append(order["order_id"])
        return orderID_list

    def cancel_uncomplete_orders(self, instrument_id):
        orderID_list = self.get_uncomplete_order(instrument_id)
        for orderID in orderID_list:
            self.revoke_order(instrument_id, orderID)

    def twenty_loss_cut(self):
        #TODO: implement loss control within 20%
        pass

    # query order info
    def get_order_info(self, instrument_id,order_id='', client_oid=''):
        if order_id:
            return self._request_without_params(GET, FUTURE_ORDER_INFO + str(instrument_id) + '/' + str(order_id))
        elif client_oid:
            return self._request_without_params(GET, FUTURE_ORDER_INFO + str(instrument_id) + '/' + str(client_oid))

    # query fills
    def get_fills(self, order_id, instrument_id, froms='', to='', limit=''):
        params = {'order_id': order_id, 'instrument_id': instrument_id}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request(GET, FUTURE_FILLS, params)

    # get products info
    def get_products(self):
        return self._request_without_params(GET, FUTURE_PRODUCTS_INFO)

    # get depth
    def get_depth(self, instrument_id, size):
        params = {'size': size}
        return self._request(GET, FUTURE_DEPTH + str(instrument_id) + '/book', params)

    # get ticker
    def get_ticker(self):
        return self._request_without_params(GET, FUTURE_TICKER)

    # get specific ticker
    def get_specific_ticker(self, instrument_id):
        return self._request_without_params(GET, FUTURE_SPECIFIC_TICKER + str(instrument_id) + '/ticker')

    # query trades
    #def get_trades(self, instrument_id, before, after, limit):
    #    params = {'before': before, 'after': after, 'limit': limit}
    #    return self._request(GET, FUTURE_TRADES + str(instrument_id) + '/trades', params, cursor=True)

    # query trades v3
    def get_trades(self, instrument_id, froms=0, to=0, limit=0):
        params = {'instrument_id': instrument_id}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request(GET, FUTURE_TRADES + str(instrument_id) + '/trades', params, cursor=True)

    # query k-line
    def get_kline(self, instrument_id, granularity, start='', end=''):
        params = {'granularity': granularity, 'start': start, 'end': end}
        return self._request(GET, FUTURE_KLINE + str(instrument_id) + '/candles', params)

    # query index
    def get_index(self, instrument_id):
        return self._request_without_params(GET, FUTURE_INDEX + str(instrument_id) + '/index')

    # query rate
    def get_rate(self):
        return self._request_without_params(GET, FUTURE_RATE)

    # query estimate price
    def get_estimated_price(self, instrument_id):
        return self._request_without_params(GET, FUTURE_ESTIMAT_PRICE + str(instrument_id) + '/estimated_price')

    # query the total platform of the platform
    def get_holds(self, instrument_id):
        return self._request_without_params(GET, FUTURE_HOLDS + str(instrument_id) + '/open_interest')

    # query limit price
    def get_limit(self, instrument_id):
        return self._request_without_params(GET, FUTURE_LIMIT + str(instrument_id) + '/price_limit')

    # query limit price
    def get_liquidation(self, instrument_id, status='1', froms = 0, to = 0, limit = 0):
        params = {'status': status}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_without_params(GET, FUTURE_LIQUIDATION + str(instrument_id) + '/liquidation')

    # query holds amount
    def get_holds_amount(self, instrument_id):
        return self._request_without_params(GET, HOLD_AMOUNT+ str(instrument_id) + '/holds')

    # query mark price
    def get_mark_price(self, instrument_id):
        return self._request_without_params(GET, FUTURE_MARK +str(instrument_id) + '/mark_price')

    def market_close_all(self, instrument_id, direction):
        params = {"instrument_id": instrument_id, "direction": direction}
        return self._request(POST, FUTURE_MARKET_CLOSE, params)

    def market_close_all_direction(self, instrument_id):
        param1 = {"instrument_id": instrument_id, "direction": "long"}
        param2 = {"instrument_id": instrument_id, "direction": "short"}
        self._request(POST, FUTURE_MARKET_CLOSE, param1)
        self._request(POST, FUTURE_MARKET_CLOSE, param2)

    #just cancel closed orders
    def cancel_all(self, instrument_id, direction):
        params = {"instrument_id": instrument_id, "direction": direction}
        return self._request(POST, FUTURE_CANCEL_ALL, params)

    #just cancel all closed orders
    def cancel_all_direction(self, instrument_id):
        param1 = {"instrument_id": instrument_id, "direction": "long"}
        param2 = {"instrument_id": instrument_id, "direction": "short"}
        self._request(POST, FUTURE_CANCEL_ALL, param1)
        self._request(POST, FUTURE_CANCEL_ALL, param2)


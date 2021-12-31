from cryptofolio.graphql_api.resolvers.binance import binance_spot_limit_order_resolver, binance_spot_market_order_resolver
from cryptofolio.graphql_api.resolvers.binance.order_resolvers import binance_spot_stop_loss_limit_order_resolver


def spot_limit_order_resolver(info, obj, exchange, authToken, order):

    if exchange == "binance":
        return binance_spot_limit_order_resolver(None, None, authToken, order)
    elif exchange == "bybit":
        return {
            'success': True,
            'status': 'FILLED'
        }
    else:
        return {
            'success': False,
            'msg': "Exchange doesn't exist"
        }


def spot_market_order_resolver(info, obj, exchange, authToken, order):

    if exchange == "binance":
        return binance_spot_market_order_resolver(None, None, authToken, order)
    elif exchange == "bybit":
        return {
            'success': True,
            'status': 'FILLED'
        }
    else:
        return {
            'success': False,
            'msg': "Exchange doesn't exist"
        }


def spot_stop_loss_limit_order_resolver(info, obj, exchange, authToken, order):

    if exchange == "binance":
        return binance_spot_stop_loss_limit_order_resolver(None, None, authToken, order)
    elif exchange == "bybit":
        return {
            'success': True,
            'status': 'FILLED'
        }
    else:
        return {
            'success': False,
            'msg': "Exchange doesn't exist"
        }

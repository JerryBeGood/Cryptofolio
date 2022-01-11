from cryptofolio.graphql_api.resolvers.binance import binance_spot_limit_order, binance_spot_market_order
from cryptofolio.graphql_api.resolvers.binance.orders import binance_spot_stop_loss_limit_order
from cryptofolio.graphql_api.resolvers.bybit.orders import bybit_spot_limit_order, bybit_spot_market_order


def spot_limit_order_resolver(obj, info, exchange, authToken, order):
    if exchange == "binance":
        return binance_spot_limit_order(authToken, order)
    elif exchange == "bybit":
        return bybit_spot_limit_order(authToken, order)
    else:
        return {
            'success': False,
            'msg': "Exchange doesn't exist"
        }


def spot_market_order_resolver(obj, info, exchange, authToken, order):

    if exchange == "binance":
        return binance_spot_market_order(authToken, order)
    elif exchange == "bybit":
        return bybit_spot_market_order(authToken, order)
    else:
        return {
            'success': False,
            'msg': "Exchange doesn't exist"
        }


def spot_stop_loss_limit_order_resolver(obj, info, exchange, authToken, order):

    if exchange == "binance":
        return binance_spot_stop_loss_limit_order(authToken, order)
    elif exchange == "bybit":
        return {
            'success': False,
            'msg': f'This order is not implemented for {exchange} exchange'
        }
    else:
        return {
            'success': False,
            'msg': "Exchange doesn't exist"
        }

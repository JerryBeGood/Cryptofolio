from cryptofolio.graphql_api.resolvers.binance import binance_exchange_info, binance_account_info, binance_open_orders
from cryptofolio.graphql_api.resolvers.bybit import bybit_exchange_info, bybit_account_info, bybit_open_orders


def open_orders_resolver(obj, info, exchange, authToken):
    if exchange == 'binance':
        return binance_open_orders(authToken)
    elif exchange == 'bybit':
        return bybit_open_orders(authToken)


def account_info_resolver(obj, info, exchange, authToken):
    if exchange == 'binance':
        return binance_account_info(authToken)
    elif exchange == 'bybit':
        return bybit_account_info(authToken)


def exchange_info_resolver(obj, info, exchange, symbols=None):
    if exchange == 'binance':
        return binance_exchange_info(symbols)
    elif exchange == 'bybit':
        return bybit_exchange_info(symbols)

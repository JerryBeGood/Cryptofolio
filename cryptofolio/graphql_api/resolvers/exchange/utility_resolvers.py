from cryptofolio.graphql_api.resolvers.binance import binance_exchange_info
from cryptofolio.graphql_api.resolvers.bybit import bybit_exchange_info


def exchange_info_resolver(obj, info, exchange, symbols=None):

    if exchange == 'binance':
        return binance_exchange_info(symbols)
    elif exchange == 'bybit':
        return bybit_exchange_info(symbols)
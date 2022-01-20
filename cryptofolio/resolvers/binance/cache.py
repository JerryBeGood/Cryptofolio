from cryptofolio.resolvers.shared_utilities import prepare_binance_exchange_info, prepare_binance_asset_ticker_info


BINANCE_EXCHANGE_INFO = prepare_binance_exchange_info()
BINANCE_ASSET_TICKER_INFO = prepare_binance_asset_ticker_info()
BINANCE_ORDERS_INFO = []


def update_binance_order_info(symbol):
    if symbol not in BINANCE_ORDERS_INFO:
        BINANCE_ORDERS_INFO.append(symbol)

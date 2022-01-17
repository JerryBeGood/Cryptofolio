from cryptofolio.graphql_api.resolvers.binance import binance_exchange_info, binance_account_info, binance_open_orders, binance_closed_orders
from cryptofolio.graphql_api.resolvers.bybit import bybit_exchange_info, bybit_account_info, bybit_open_orders, binance_closed_orders
from cryptofolio.graphql_api.resolvers.shared_utilities import validate_token, fetch_exchange_credentials


def closed_orders_resolver(obj, info, exchange, authToken):
    # Validate token
    token_validation_payload = validate_token(authToken)
    if not token_validation_payload[0]:
        return {'success': token_validation_payload[0], 'msg': token_validation_payload[1], 'orders': []}

    # Fetch exchange credentials
    exchange_credentials = fetch_exchange_credentials(
        token_validation_payload[1], exchange)
    if not exchange_credentials[0]:
        return {'success': False, 'msg': exchange_credentials[1], 'orders': []}

    if exchange == 'binance':
        return binance_closed_orders(exchange_credentials)
    elif exchange == 'bybit':
        return bybit_closed_orders(exchange_credentials)

def open_orders_resolver(obj, info, exchange, authToken):
    # Validate token
    token_validation_payload = validate_token(authToken)
    if not token_validation_payload[0]:
        return {'success': token_validation_payload[0], 'msg': token_validation_payload[1], 'orders': []}

    # Fetch exchange credentials
    exchange_credentials = fetch_exchange_credentials(
        token_validation_payload[1], exchange)
    if not exchange_credentials[0]:
        return {'success': False, 'msg': exchange_credentials[1], 'orders': []}

    if exchange == 'binance':
        return binance_open_orders(exchange_credentials)
    elif exchange == 'bybit':
        return bybit_open_orders(exchange_credentials)


def account_info_resolver(obj, info, exchange, authToken):
    # Validate token
    token_validation_payload = validate_token(authToken)
    if not token_validation_payload[0]:
        return {'success': token_validation_payload[0], 'msg': token_validation_payload[1]}

    # Fetch exchange credentials
    exchange_credentials = fetch_exchange_credentials(
        token_validation_payload[1], exchange)
    if not exchange_credentials[0]:
        return {'success': False, 'msg': exchange_credentials[1]}

    if exchange == 'binance':
        return binance_account_info(exchange_credentials)
    elif exchange == 'bybit':
        return bybit_account_info(exchange_credentials)


def exchange_info_resolver(obj, info, exchange, symbols=None):
    if exchange == 'binance':
        return binance_exchange_info(symbols)
    elif exchange == 'bybit':
        return bybit_exchange_info(symbols)

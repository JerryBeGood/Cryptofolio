from cryptofolio.graphql_api.resolvers.binance import binance_spot_limit_order, binance_spot_market_order
from cryptofolio.graphql_api.resolvers.binance.orders import binance_spot_stop_loss_limit_order
from cryptofolio.graphql_api.resolvers.bybit.orders import bybit_spot_limit_order, bybit_spot_market_order
from cryptofolio.graphql_api.resolvers.shared_utilities import validate_token, fetch_exchange_credentials


def spot_limit_order_resolver(obj, info, exchange, authToken, order):
    # Validate token
    token_validation_payload = validate_token(authToken)
    if not token_validation_payload[0]:
        return {'success': token_validation_payload[0], 'msg': token_validation_payload[1]}

    # Fetch exchange credentials
    exchange_credentials = fetch_exchange_credentials(
        token_validation_payload[1], exchange)
    if not exchange_credentials[0]:
        return {'success': False, 'msg': exchange_credentials[1]}

    if exchange == "binance":
        return binance_spot_limit_order(exchange_credentials, order)
    elif exchange == "bybit":
        return bybit_spot_limit_order(exchange_credentials, order)
    else:
        return {
            'success': False,
            'msg': "Exchange doesn't exist"
        }


def spot_market_order_resolver(obj, info, exchange, authToken, order):
    # Validate token
    token_validation_payload = validate_token(authToken)
    if not token_validation_payload[0]:
        return {'success': token_validation_payload[0], 'msg': token_validation_payload[1]}

    # Fetch exchange credentials
    exchange_credentials = fetch_exchange_credentials(
        token_validation_payload[1], exchange)
    if not exchange_credentials[0]:
        return {'success': False, 'msg': exchange_credentials[1]}

    if exchange == "binance":
        return binance_spot_market_order(exchange_credentials, order)
    elif exchange == "bybit":
        return bybit_spot_market_order(exchange_credentials, order)
    else:
        return {
            'success': False,
            'msg': "Exchange doesn't exist"
        }


def spot_stop_loss_limit_order_resolver(obj, info, exchange, authToken, order):
    # Validate token
    token_validation_payload = validate_token(authToken)
    if not token_validation_payload[0]:
        return {'success': token_validation_payload[0], 'msg': token_validation_payload[1]}

    # Fetch exchange credentials
    exchange_credentials = fetch_exchange_credentials(
        token_validation_payload[1], exchange)
    if not exchange_credentials[0]:
        return {'success': False, 'msg': exchange_credentials[1]}

    if exchange == "binance":
        return binance_spot_stop_loss_limit_order(exchange_credentials, order)
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

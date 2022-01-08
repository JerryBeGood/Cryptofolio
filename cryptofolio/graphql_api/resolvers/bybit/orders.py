import time

from cryptofolio.graphql_api.resolvers.shared_utilities import validate_token, fetch_exchange_credentials
from .utility import make_order, make_order_signature


def bybit_spot_limit_order(authToken, order):
    return {
        'success': True,
        'status': 'FILLED'
    }


def bybit_spot_market_order(authToken, order):

    # Validate token
    token_validation_payload = validate_token(authToken)
    if not token_validation_payload[0]:
        return {'success': token_validation_payload[0], 'msg': token_validation_payload[1]}

    # Fetch exchange credentials
    exchange_credentials = fetch_exchange_credentials(
        token_validation_payload[1], 'bybit')
    if not exchange_credentials[0]:
        return {'success': False, 'msg': exchange_credentials[1]}

    # Prepare request body
    timestamp = int(round(time.time() * 1000))
    params = {
        'api_key': exchange_credentials[1],
        'side': order["side"],
        'symbol': order['symbol'],
        'timestamp': timestamp,
        'type': 'MARKET',
        'qty': order['quantity']
    }

    params['sign'] = make_order_signature(params, exchange_credentials[2])
    payload = make_order(params)

    return payload

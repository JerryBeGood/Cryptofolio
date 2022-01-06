import time
import hmac
import hashlib

from cryptofolio.graphql_api.resolvers.shared_utilities import validate_token, fetch_exchange_credentials
from .utility import make_order


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

    request_body = ""
    for key in sorted(params.keys()):
        v = params[key]
        if isinstance(params[key], bool):
            if params[key]:
                v = "true"
            else:
                v = "false"
        request_body += f"{key}={v}&"
    request_body = request_body[:-1]

    sign = hmac.new(exchange_credentials[2].encode(),
                    request_body.encode('UTF-8'),
                    digestmod=hashlib.sha256).hexdigest()

    params['sign'] = sign
    payload = make_order(params)

    return payload

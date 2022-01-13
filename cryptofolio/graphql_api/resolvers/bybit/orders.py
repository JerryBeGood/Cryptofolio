import time

from cryptofolio.graphql_api.resolvers.shared_utilities import validate_token, fetch_exchange_credentials
from .utility import make_order, make_signature


def bybit_spot_limit_order(exchange_credentials, order):
    # Prepare request body
    timestamp = int(round(time.time() * 1000))
    params = {
        'api_key': exchange_credentials[1],
        'side': order["side"],
        'symbol': order['symbol'],
        'timestamp': timestamp,
        'type': 'LIMIT',
        'qty': order['quantity'],
        'timeInForce': order['timeInForce'] if 'timeInForce' in order.keys() else 'GTC',
        'price': order['price']
    }

    params['sign'] = make_signature(params, exchange_credentials[2])
    payload = make_order(params)

    return payload


def bybit_spot_market_order(exchange_credentials, order):

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

    params['sign'] = make_signature(params, exchange_credentials[2])
    payload = make_order(params)

    return payload

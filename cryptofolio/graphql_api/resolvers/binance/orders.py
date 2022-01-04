import time
import hmac
import hashlib

from .utility import make_order
from .utility import prepare_stop_loss_order_request_body, prepare_stop_loss_order_params
from .utility import prepare_spot_market_order_request_body, prepare_spot_market_order_params
from .utility import prepare_spot_market_limit_order_params, prepare_spot_market_limit_order_request_body

from cryptofolio.graphql_api.resolvers.shared_utilities import validate_token, fetch_exchange_credentials


def binance_spot_stop_loss_limit_order(authToken,
                                                order):
    # Prepare request body
    payload = {}
    timestamp = int(round(time.time() * 1000))
    params = prepare_stop_loss_order_params(order, timestamp)
    request_body = prepare_stop_loss_order_request_body(order, timestamp)

    # Validate token
    token_validation_payload = validate_token(authToken)
    if not token_validation_payload[0]:
        return {'success': token_validation_payload[0], 'msg': token_validation_payload[1]}

    # Fetch exchange credentials
    exchange_credentials = fetch_exchange_credentials(
        token_validation_payload[1], 'binance')
    if not exchange_credentials[0]:
        return {'success': False, 'msg': exchange_credentials[1]}

    # Preapre signature
    signature = hmac.new(exchange_credentials[2].encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()
    params['signature'] = signature

    # Make a request
    payload = make_order(params, exchange_credentials[1])

    return payload


def binance_spot_market_order(authToken, order):

    payload = {}

    # Prepare request data
    timestamp = int(round(time.time() * 1000))
    params = prepare_spot_market_order_params(order, timestamp)
    request_body = prepare_spot_market_order_request_body(order, timestamp)

    # Validate token
    token_validation_payload = validate_token(authToken)
    if not token_validation_payload[0]:
        return {'success': token_validation_payload[0], 'msg': token_validation_payload[1]}

    # Fetch exchange credentials
    exchange_credentials = fetch_exchange_credentials(
        token_validation_payload[1], 'binance')
    if not exchange_credentials[0]:
        return {'success': False, 'msg': exchange_credentials[1]}

    signature = hmac.new(exchange_credentials[2].encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()
    params['signature'] = signature

    # Make a request
    payload = make_order(params, exchange_credentials[1])

    return payload


def binance_spot_limit_order(authToken, order):

    payload = {}
    # Prepare request data
    timestamp = int(round(time.time() * 1000))
    params = prepare_spot_market_limit_order_params(order, timestamp)
    request_body = prepare_spot_market_limit_order_request_body(order, timestamp)

    # Validate token
    token_validation_payload = validate_token(authToken)
    if not token_validation_payload[0]:
        return {'success': token_validation_payload[0], 'msg': token_validation_payload[1]}

    # Fetch exchange credentials
    exchange_credentials = fetch_exchange_credentials(
        token_validation_payload[1], 'binance')
    if not exchange_credentials[0]:
        return {'success': False, 'msg': exchange_credentials[1]}

    signature = hmac.new(exchange_credentials[2].encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()
    params['signature'] = signature

    # Make a request
    payload = make_order(params, exchange_credentials[1])

    return payload

import time
import hmac
import hashlib

from .utility import make_order
from .utility import prepare_stop_loss_order_request_body, prepare_stop_loss_order_params
from .utility import prepare_spot_market_order_request_body, prepare_spot_market_order_params
from .utility import prepare_spot_market_limit_order_params, prepare_spot_market_limit_order_request_body

from cryptofolio.graphql_api.resolvers.shared_utilities import validate_token, fetch_exchange_credentials


def binance_spot_stop_loss_limit_order(exchange_credentials, order):
    # Prepare request body
    payload = {}
    timestamp = int(round(time.time() * 1000))
    params = prepare_stop_loss_order_params(order, timestamp)
    request_body = prepare_stop_loss_order_request_body(order, timestamp)

    # Preapre signature
    signature = hmac.new(exchange_credentials[2].encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()
    params['signature'] = signature

    # Make a request
    payload = make_order(params, exchange_credentials[1])

    return payload


def binance_spot_market_order(exchange_credentials, order):

    payload = {}

    # Prepare request data
    timestamp = int(round(time.time() * 1000))
    params = prepare_spot_market_order_params(order, timestamp)
    request_body = prepare_spot_market_order_request_body(order, timestamp)

    signature = hmac.new(exchange_credentials[2].encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()
    params['signature'] = signature

    # Make a request
    payload = make_order(params, exchange_credentials[1])

    return payload


def binance_spot_limit_order(exchange_credentials, order):

    payload = {}
    # Prepare request data
    timestamp = int(round(time.time() * 1000))
    params = prepare_spot_market_limit_order_params(order, timestamp)
    request_body = prepare_spot_market_limit_order_request_body(
        order, timestamp)

    signature = hmac.new(exchange_credentials[2].encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()
    params['signature'] = signature

    # Make a request
    payload = make_order(params, exchange_credentials[1])

    return payload

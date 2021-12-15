import requests
import time
import hmac
import hashlib

from .order_utility import prepare_stop_loss_order_request_body, prepare_stop_loss_order_params
from .order_utility import prepare_spot_market_order_request_body, prepare_spot_market_order_params

from cryptofolio.utilities import validate_token, fetch_exchange_credentials


def binance_spot_stop_loss_limit_order_resolver(obj, info, authToken,
                                                order):
    # Prepare request body
    payload = {}
    timestamp = int(round(time.time() * 1000))
    params = prepare_stop_loss_order_params(order, timestamp)
    request_body = prepare_stop_loss_order_request_body(order, timestamp)

    # Validate token
    token_validation_payload = validate_token(authToken)
    print(token_validation_payload)
    if not token_validation_payload[0]:
        return {'succes': token_validation_payload[0], 'msg': token_validation_payload[1]}

    # Fetch exchange credentials
    exchange_credentials = fetch_exchange_credentials(
        token_validation_payload[1], 'binance')
    print(exchange_credentials)
    if not exchange_credentials[0]:
        return {'succes': False, 'msg': exchange_credentials[1]}

    # Preapre signature
    signature = hmac.new(exchange_credentials[2].encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()
    params['signature'] = signature

    # Make a request
    with requests.post('https://testnet.binance.vision/api/v3/order',
                       params=params,
                       headers={
                           'X-MBX-APIKEY': exchange_credentials[1],
                           'content-type': 'application/x-www-form-urlencoded'
                       }) as response:

        response_json = response.json()
        print(f'RESPONSE: {response_json}')

        if response.status_code != 200:
            payload['succes'] = False
            payload['code'] = response_json['code']
            payload['msg'] = response_json['msg']
        else:
            payload['succes'] = True
            payload['status'] = response_json['status']

    return payload


def binance_spot_market_order_resolver(obj, info, authToken, order):

    payload = {}

    # Prepare request data
    timestamp = int(round(time.time() * 1000))
    params = prepare_spot_market_order_params(order, timestamp)
    request_body = prepare_spot_market_order_request_body(order, timestamp)

    # Validate token
    token_validation_payload = validate_token(authToken)
    print(token_validation_payload)
    if not token_validation_payload[0]:
        return {'success': token_validation_payload[0], 'msg': token_validation_payload[1]}

    # Fetch exchange credentials
    exchange_credentials = fetch_exchange_credentials(
        token_validation_payload[1], 'binance')
    print(exchange_credentials)
    if not exchange_credentials[0]:
        return {'succes': False, 'msg': exchange_credentials[1]}

    signature = hmac.new(exchange_credentials[2].encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()
    params['signature'] = signature

    with requests.post('https://testnet.binance.vision/api/v3/order',
                       params=params,
                       headers={
                           'X-MBX-APIKEY': exchange_credentials[1],
                           'content-type': 'application/x-www-form-urlencoded'
                       }) as response:

        response_json = response.json()

        print(response_json)
        if response.status_code != 200:
            payload['succes'] = False
            payload['code'] = response_json['code']
            payload['msg'] = response_json['msg']
        else:
            payload['succes'] = True
            payload['status'] = response_json['status']

    return payload


def binance_spot_limit_order_resolver(info, obj, API_key, secret, order):

    payload = {}
    params = {}
    request_body = ''
    timestamp = int(round(time.time() * 1000))

    if 'icebergQty' in order.keys():
        request_body = f'symbol={order["symbol"]}&side={order["side"]}&type=LIMIT&icebergQty={order["icebergQty"]}&quantity={order["quantity"]}&timeInForce={order["timeInForce"]}&price={order["price"]}&timestamp={timestamp}'
        params['symbol'] = order["symbol"]
        params['side'] = order["side"]
        params['type'] = 'LIMIT'
        params['icebergQty'] = order['icebergQty']
        params['quantity'] = order['quantity']
        params['timeInForce'] = order['timeInForce']
        params['price'] = order['price']
        params['timestamp'] = timestamp
    else:
        request_body = f'symbol={order["symbol"]}&side={order["side"]}&type=LIMIT&quantity={order["quantity"]}&timeInForce={order["timeInForce"]}&price={order["price"]}&timestamp={timestamp}'
        params['symbol'] = order["symbol"]
        params['side'] = order["side"]
        params['type'] = 'LIMIT'
        params['quantity'] = order['quantity']
        params['timeInForce'] = order['timeInForce']
        params['price'] = order['price']
        params['timestamp'] = timestamp

    signature = hmac.new(secret.encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()

    params['signature'] = signature

    with requests.post('https://testnet.binance.vision/api/v3/order',
                       params=params,
                       headers={
                           'X-MBX-APIKEY': API_key,
                           'content-type': 'application/x-www-form-urlencoded'
                       }) as response:

        response_json = response.json()

        if response.status_code != 200:
            payload['succes'] = False
            payload['code'] = response_json['code']
            payload['msg'] = response_json['msg']
        else:
            payload['succes'] = True
            payload['status'] = response_json['status']

    return payload

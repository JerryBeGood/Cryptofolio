import requests
import time
import hmac, hashlib


def binance_spot_stop_loss_limit_order_resolver(obj, info, API_key, secret,
                                                order):
    payload = {}
    params = {}
    request_body = ''
    timestamp = int(round(time.time() * 1000))

    if 'icebergQty' in order.keys():
        request_body = f'symbol={order["symbol"]}&side={order["side"]}&type=STOP_LOSS_LIMIT&icebergQty={order["icebergQty"]}&quantity={order["quantity"]}&timeInForce={order["timeInForce"]}&price={order["price"]}&stopPrice={order["stopPrice"]}&newOrderRespType=RESULT&timestamp={timestamp}'
        params['symbol'] = order["symbol"]
        params['side'] = order["side"]
        params['type'] = 'STOP_LOSS_LIMIT'
        params['icebergQty'] = order['icebergQty']
        params['quantity'] = order['quantity']
        params['timeInForce'] = order['timeInForce']
        params['price'] = order['price']
        params['stopPrice'] = order['stopPrice']
        params['newOrderRespType'] = 'RESULT'
        params['timestamp'] = timestamp
    else:
        request_body = f'symbol={order["symbol"]}&side={order["side"]}&type=STOP_LOSS_LIMIT&quantity={order["quantity"]}&timeInForce={order["timeInForce"]}&price={order["price"]}&stopPrice={order["stopPrice"]}&newOrderRespType=RESULT&timestamp={timestamp}'
        params['symbol'] = order["symbol"]
        params['side'] = order["side"]
        params['type'] = 'STOP_LOSS_LIMIT'
        params['quantity'] = order['quantity']
        params['timeInForce'] = order['timeInForce']
        params['price'] = order['price']
        params['stopPrice'] = order['stopPrice']
        params['newOrderRespType'] = 'RESULT'
        params['timestamp'] = timestamp
    signature = hmac.new(secret.encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()

    params['signature'] = signature

    with requests.post('https://api1.binance.com/api/v3/order',
                       params=params,
                       headers={
                           'X-MBX-APIKEY': API_key,
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


def binance_spot_market_order_resolver(obj, info, API_key, secret, order):

    payload = {}
    params = {}
    request_body = ''
    timestamp = int(round(time.time() * 1000))

    if order['base'] == True:
        request_body = f'symbol={order["symbol"]}&side={order["side"]}&type=MARKET&quantity={order["quantity"]}&timestamp={timestamp}'
        params['symbol'] = order["symbol"]
        params['side'] = order["side"]
        params['type'] = 'MARKET'
        params['quantity'] = order['quantity']
        params['timestamp'] = timestamp
    else:
        request_body = f'symbol={order["symbol"]}&side={order["side"]}&type=MARKET&quoteOrderQty={order["quantity"]}&timestamp={timestamp}'
        params['symbol'] = order["symbol"]
        params['side'] = order["side"]
        params['type'] = 'MARKET'
        params['quoteOrderQty'] = order['quantity']
        params['timestamp'] = timestamp

    signature = hmac.new(secret.encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()

    params['signature'] = signature

    with requests.post('https://api1.binance.com/api/v3/order',
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

    with requests.post('https://api1.binance.com/api/v3/order',
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
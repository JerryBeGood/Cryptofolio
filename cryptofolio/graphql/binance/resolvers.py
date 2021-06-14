import requests
import time
import hmac, hashlib

from cryptofolio.utility import EXCHANGE_INFO


# binanceAccountInfo query resolver
def resolve_binanceAccountInfo(obj, info, API_key, secret, recvWindow=5000):

    payload = {}

    timestamp = int(round(time.time() * 1000))
    request_body = f'recvWindow={recvWindow}&timestamp={timestamp}'
    signature = hmac.new(secret.encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()

    with requests.get(f'https://testnet.binance.vision/api/v3/account',
                      params={
                          'recvWindow': recvWindow,
                          'timestamp': timestamp,
                          'signature': signature
                      },
                      headers={'X-MBX-APIKEY': API_key}) as response:

        response_json = response.json()

        payload['succes'] = True
        payload['errors'] = ""
        payload['accountType'] = response_json['accountType']
        payload['balances'] = []

        for asset in response_json['balances']:
            balance = {}
            balance['asset'] = asset['asset']
            balance['free'] = asset['free']
            balance['locked'] = asset['locked']

            payload['balances'].append(balance)

    return payload


# binanceExchangeInfo query resolver
def resolve_binanceExchangeInfo(obj, info, symbols=None):

    keys = EXCHANGE_INFO.keys()
    payload = []

    if symbols == None:
        payload = EXCHANGE_INFO.values()
    else:
        for symbol in symbols:
            if symbol in keys:
                payload.append(EXCHANGE_INFO[symbol])

    return payload


# binanceSPOTMarketOrder mutation resolver
def resolve_binanceSPOTMarketOrder(obj, info, API_key, secret, order):

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


# binanceSPOTLimitOrder mutation resolver
def resolve_binanceSPOTLimiOrder(info, obj, API_key, secret, order):

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
import requests
import time
import hmac, hashlib
from cryptofolio import binance_exchange_info

from cryptofolio import binance_exchange_info


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

    keys = binance_exchange_info.keys()
    payload = []

    if symbols == None:
        payload = binance_exchange_info.values()
    else:
        for symbol in symbols:
            if symbol in keys:
                payload.append(binance_exchange_info[symbol])

    return payload

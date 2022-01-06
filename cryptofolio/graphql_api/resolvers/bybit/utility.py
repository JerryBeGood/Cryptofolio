import time
import requests
import hmac
import hashlib

from cryptofolio.graphql_api.resolvers.shared_utilities import bybit_exchange_info

BYBIT_EXCHANGE_INFO = bybit_exchange_info()


def make_order(params):

    payload = {}

    with requests.post('https://api-testnet.bybit.com/spot/v1/order',
                       params=params,
                       headers={
                           "Content-Type": "application/x-www-form-urlencoded"
                       }) as response:

        print(response.url)
        response_json = response.json()

        print(response_json)

        if response.status_code != 200:
            payload['success'] = False
            payload['code'] = response_json['ret_code']
            payload['msg'] = response_json['ret_msg']
        else:
            payload['success'] = True
            payload['status'] = response_json['result']['status']

    return payload


def validate_bybit_credentials(API_key, secret):

    timestamp = int(round(time.time() * 1000))
    request_body = f'api_key={API_key}&timestamp={timestamp}'
    sign = hmac.new(secret.encode(),
                    request_body.encode('UTF-8'),
                    digestmod=hashlib.sha256).hexdigest()

    with requests.get(f'https://api-testnet.bybit.com/spot/v1/account',
                      params={
                          'api_key': API_key,
                          'timestamp': timestamp,
                          'sign': sign
                      }) as response:

        if response.status_code == 200:
            return True, response
        else:
            return False, response


def bybit_exchange_info(symbols=None):

    keys = BYBIT_EXCHANGE_INFO.keys()
    payload = []

    if symbols is None:
        for pair in BYBIT_EXCHANGE_INFO.values():
            asset_pair = {}
            asset_pair['symbol'] = pair['name']
            asset_pair['baseAsset'] = pair['baseCurrency']
            asset_pair['quoteAsset'] = pair['quoteCurrency']
            payload.append(asset_pair)
    else:
        for symbol in symbols:
            if symbol in keys:
                asset_pair = {}
                asset_pair['symbol'] = BYBIT_EXCHANGE_INFO[symbol]['name']
                asset_pair['baseAsset'] = BYBIT_EXCHANGE_INFO[symbol]['baseCurrency']
                asset_pair['quoteAsset'] = BYBIT_EXCHANGE_INFO[symbol]['quoteCurrency']
                payload.append(asset_pair)

    return payload

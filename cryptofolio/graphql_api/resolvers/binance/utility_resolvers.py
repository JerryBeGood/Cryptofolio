import requests
import time
import hmac
import hashlib

from cryptofolio.utilities import EXCHANGE_INFO, ASSET_TICKER_INFO


def binance_account_info_resolver(obj, info, API_key, secret, recvWindow=5000):
    payload = {}
    payload['totalValue'] = 0.0
    payload['valueChangePercentage'] = 0.0
    payload['balances'] = []

    response_json = binance_account_info_request(API_key, secret, recvWindow)

    for asset in response_json['balances']:
        balance = {}
        balance['asset'] = asset['asset']

        if asset['asset'] in ['USDT', 'BUSD']:
            balance['percentage'] = float(asset['free'])
            payload['totalValue'] += balance['percentage']
        else:
            if f'{asset["asset"]}USDT' in ASSET_TICKER_INFO.keys():
                balance['percentage'] = float(
                    ASSET_TICKER_INFO[f'{asset["asset"]}USDT']
                    ['price']) * float(asset['free'])
            else:
                balance['percentage'] = None

            payload['totalValue'] += balance['percentage']

        payload['balances'].append(balance)

    for asset in payload['balances']:
        if asset['asset'] not in ['USDT', 'BUSD']:
            payload['valueChangePercentage'] += float(
                ASSET_TICKER_INFO[f'{asset["asset"]}USDT']
                ['priceChangePercent']) * (asset['percentage'] / 100)
        asset['percentage'] = round(
            asset['percentage'] / (payload['totalValue'] / 100), 2)

    payload['totalValue'] = round(payload['totalValue'], 2)
    payload['valueChangePercentage'] = round(
        payload['valueChangePercentage'] / (payload['totalValue'] / 100), 2)

    return payload


def binance_exchange_info_resolver(obj, info, symbols=None):

    keys = EXCHANGE_INFO.keys()
    payload = []

    if symbols is None:
        payload = EXCHANGE_INFO.values()
    else:
        for symbol in symbols:
            if symbol in keys:
                payload.append(EXCHANGE_INFO[symbol])

    return payload


def binance_account_info_request(API_key, secret, recvWindow):
    timestamp = int(round(time.time() * 1000))
    request_body = f'recvWindow={recvWindow}&timestamp={timestamp}'
    signature = hmac.new(secret.encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()

    with requests.get(f'https://api1.binance.com/api/v3/account',
                      params={
                          'recvWindow': recvWindow,
                          'timestamp': timestamp,
                          'signature': signature
                      },
                      headers={'X-MBX-APIKEY': API_key}) as response:

        return response.json()

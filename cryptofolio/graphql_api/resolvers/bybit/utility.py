import time
import datetime
import requests
import hmac
import hashlib

from pytz import timezone

from cryptofolio.graphql_api.resolvers.shared_utilities import bybit_asset_ticker_info, bybit_exchange_info
from cryptofolio import app

BYBIT_EXCHANGE_INFO = bybit_exchange_info()
BYBIT_ASSET_TICKER_INFO = bybit_asset_ticker_info()


def bybit_open_orders(exchange_credentials):

    timestamp = int(round(time.time() * 1000))
    params = {
        'api_key': exchange_credentials[1],
        'timestamp': timestamp,
    }
    params['sign'] = make_signature(params, exchange_credentials[2])

    with requests.get(f'{app.config.get("BYBIT")}/spot/v1/open-orders',
                      params=params) as response:

        payload = {}
        response_json = response.json()

        if response_json['ret_code'] == 0:
            payload['success'] = True
            payload['msg'] = 'Ok'
            payload['orders'] = prepare_open_orders_data(
                response_json)
        else:
            payload['success'] = False
            payload['msg'] = response_json['ret_msg']
            payload['orders'] = []

        return payload


def bybit_account_info(exchange_credentials):

    timestamp = int(round(time.time() * 1000))
    params = {
        'api_key': exchange_credentials[1],
        'timestamp': timestamp,
    }
    params['sign'] = make_signature(params, exchange_credentials[2])

    with requests.get(f'{app.config.get("BYBIT")}/spot/v1/account',
                      params=params) as response:

        payload = {}
        response_json = response.json()

        if response_json['ret_code'] == 0:
            payload['success'] = True
            payload['msg'] = 'Ok'
            payload['AccountInformation'] = prepare_account_info_data(
                response_json)
        else:
            payload['success'] = False
            payload['msg'] = response_json['ret_msg']

        return payload


def prepare_open_orders_data(response_json):
    orders = []
    for position in response_json['result']:
        order = {}
        order['pair'] = position['symbol']
        order['type'] = position['type']
        order['side'] = position['side']
        order['price'] = position['price']
        order['origQty'] = position['origQty']
        order['execQty'] = position['executedQty']
        order['status'] = position['status']
        order['time'] = datetime.datetime.fromtimestamp(
            int(position['time'])//1000, timezone('Europe/Warsaw'))
        orders.append(order)

    return orders


def prepare_account_info_data(response_json):

    account_information = {}
    account_information['totalValue'] = 0.0
    account_information['valueChangePercentage'] = 0.0
    account_information['balances'] = []

    for balance in response_json['result']['balances']:
        if balance['free'] != 0.0 and balance['free'] is not None:
            asset = {}
            asset['asset'] = balance['coin']

            if asset['asset'] == 'USDT':
                asset['quantity'] = round(float(balance['free']), 3)
                asset['value'] = asset['quantity']
                account_information['totalValue'] += float(
                    round(asset['value'], 3))
            else:
                asset['quantity'] = round(float(balance['free']), 3)
                asset['value'] = round(asset['quantity'] * float(
                    BYBIT_ASSET_TICKER_INFO[f"{asset['asset']}USDT"]['price']), 3)
                account_information['totalValue'] += float(
                    round(asset['value'], 3))

            account_information['balances'].append(asset)

    if account_information['totalValue'] != 0:
        for balance in account_information['balances']:
            balance['percentage'] = round(
                balance['value'] / (account_information['totalValue'] / 100), 3)

        for balance in account_information['balances']:
            balance_change = day_change_percentage(
                symbol=f"{balance['asset']}USDT")
            balance_change_value = balance_change * (balance['value'] / 100)
            account_information['valueChangePercentage'] += balance_change_value

        account_information['valueChangePercentage'] = round(
            account_information['valueChangePercentage'] / (account_information['totalValue'] / 100), 3) - 100

    return account_information


def day_change_percentage(symbol: str):

    payload = 0

    with requests.get(
            url=f'{app.config.get("BYBIT")}/spot/quote/v1/kline',
            params={
                'symbol': symbol,
                'interval': '1d',
                'limit': 1
            }) as response:

        response_json = response.json()

        if response_json['ret_code'] == 0:
            open = float(response_json['result'][0][1])
            close = float(response_json['result'][0][4])

            payload = round(close / (open / 100) - 100, 3)

    return payload


def make_signature(params, secret):
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

    signature = hmac.new(secret.encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()

    return signature


def make_order(params):

    payload = {}

    with requests.post(f'{app.config.get("BYBIT")}/spot/v1/order',
                       params=params,
                       headers={
                           "Content-Type": "application/x-www-form-urlencoded"
                       }) as response:

        response_json = response.json()

        if response_json['ret_code'] == 0:
            payload['success'] = True
            payload['status'] = response_json['result']['status']
        else:
            payload['success'] = False
            payload['code'] = response_json['ret_code']
            payload['msg'] = response_json['ret_msg']

    return payload


def validate_bybit_credentials(API_key, secret):

    timestamp = int(round(time.time() * 1000))
    request_body = f'api_key={API_key}&timestamp={timestamp}'
    sign = hmac.new(secret.encode(),
                    request_body.encode('UTF-8'),
                    digestmod=hashlib.sha256).hexdigest()

    with requests.get(f'{app.config.get("BYBIT")}/spot/v1/account',
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

import requests
import time
import datetime
import hmac
import hashlib

from pytz import timezone


from cryptofolio import app
from cryptofolio.resolvers.shared_utilities import prepare_start_time
from .cache import BINANCE_EXCHANGE_INFO, BINANCE_ASSET_TICKER_INFO, BINANCE_ORDERS_INFO
from .cache import update_binance_order_info


def binance_closed_orders(exchange_credentials):
    payload = {}
    payload['orders'] = []

    for symbol in BINANCE_ORDERS_INFO:
        timestamp = int(round(time.time() * 1000))
        startTime = prepare_start_time()
        request_body = f'symbol={symbol}&startTime={startTime}&recvWindow=5000&timestamp={timestamp}'
        signature = hmac.new(exchange_credentials[2].encode(),
                             request_body.encode('UTF-8'),
                             digestmod=hashlib.sha256).hexdigest()

        with requests.get(f'{app.config.get("BINANCE")}/api/v3/allOrders',
                          params={
                              'symbol': symbol,
                              'startTime': startTime,
                              'recvWindow': 5000,
                              'timestamp': timestamp,
                              'signature': signature
                          },
                          headers={'X-MBX-APIKEY': exchange_credentials[1]}) as response:

            response_json = response.json()

            if response.status_code == 200:
                payload['orders'] += prepare_closed_orders_data(response_json)

    payload['success'] = True
    payload['msg'] = 'Ok'

    return payload


def binance_open_orders(exchange_credentials):
    payload = {}
    timestamp = int(round(time.time() * 1000))
    request_body = f'recvWindow=5000&timestamp={timestamp}'
    signature = hmac.new(exchange_credentials[2].encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()

    with requests.get(f'{app.config.get("BINANCE")}/api/v3/openOrders',
                      params={
                          'recvWindow': 5000,
                          'timestamp': timestamp,
                          'signature': signature
                      },
                      headers={'X-MBX-APIKEY': exchange_credentials[1]}) as response:

        response_json = response.json()

        if response.status_code != 200:
            payload['success'] = False
            payload['msg'] = response_json['msg']
            payload['orders'] = []
        else:
            payload['success'] = True
            payload['msg'] = 'Ok'
            payload['orders'] = prepare_open_orders_data(response_json)

    return payload


def binance_account_info(exchange_credentials):

    payload = {}
    timestamp = int(round(time.time() * 1000))
    request_body = f'recvWindow=5000&timestamp={timestamp}'
    signature = hmac.new(exchange_credentials[2].encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()

    with requests.get(f'{app.config.get("BINANCE")}/api/v3/account',
                      params={
                          'recvWindow': 5000,
                          'timestamp': timestamp,
                          'signature': signature
                      },
                      headers={'X-MBX-APIKEY': exchange_credentials[1]}) as response:

        response_json = response.json()

        if response.status_code != 200:
            payload['success'] = False
            payload['msg'] = response_json['msg']
        else:
            payload['success'] = True
            payload['msg'] = 'Ok'
            payload['AccountInformation'] = binance_prepare_account_info_data(
                response_json)

        return payload


def binance_exchange_info(symbols=None):

    keys = BINANCE_EXCHANGE_INFO.keys()
    payload = []

    if symbols is None:
        payload = BINANCE_EXCHANGE_INFO.values()
    else:
        for symbol in symbols:
            if symbol in keys:
                payload.append(BINANCE_EXCHANGE_INFO[symbol])

    return payload


def prepare_open_orders_data(response_json):
    orders = []
    for position in response_json:
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

        update_binance_order_info(position['symbol'])

    return orders


def prepare_closed_orders_data(response_json):
    orders = []
    for position in response_json:
        if position['status'] in ['CANCELED', 'EXPIRED', 'FILLED']:
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


def validate_binance_credentials(API_key, secret):
    recvWindow = 5000
    timestamp = int(round(time.time() * 1000))
    request_body = f'recvWindow={recvWindow}&timestamp={timestamp}'
    signature = hmac.new(secret.encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()

    with requests.get(f'{app.config.get("BINANCE")}/api/v3/account',
                      params={
                          'recvWindow': recvWindow,
                          'timestamp': timestamp,
                          'signature': signature
                      },
                      headers={'X-MBX-APIKEY': API_key}) as response:

        if response.status_code == 200:
            return True, response
        else:
            return False, response


def binance_prepare_account_info_data(response_json):
    account_information = {}
    account_information['totalValue'] = 0.0
    account_information['valueChangePercentage'] = 0.0
    account_information['balances'] = []

    for asset in response_json['balances']:
        balance = {}
        balance['asset'] = asset['asset']
        balance['quantity'] = round(float(asset['free']), 5)

        if balance['quantity'] != 0.0 and balance['quantity'] is not None:

            if asset['asset'] in ['USDT', 'BUSD']:
                balance['value'] = round(balance['quantity'], 5)
                account_information['totalValue'] += balance['value']
            else:
                if f'{asset["asset"]}USDT' in BINANCE_ASSET_TICKER_INFO.keys():
                    update_binance_order_info(f'{asset["asset"]}USDT')
                    balance['value'] = round(float(
                        BINANCE_ASSET_TICKER_INFO[f'{asset["asset"]}USDT']
                        ['price']) * float(asset['free']), 5)
                    account_information['totalValue'] += balance['value']
                else:
                    balance['percentage'] = None

            account_information['balances'].append(balance)

    if account_information['totalValue'] != 0.0:
        for asset in account_information['balances']:
            if asset['asset'] not in ['USDT', 'BUSD']:
                account_information['valueChangePercentage'] += float(
                    BINANCE_ASSET_TICKER_INFO[f'{asset["asset"]}USDT']
                    ['priceChangePercent']) * (asset['value'] / 100)
            asset['percentage'] = round(
                asset['value'] / (account_information['totalValue'] / 100), 2)

        account_information['totalValue'] = round(
            account_information['totalValue'], 2)
        account_information['valueChangePercentage'] = round(
            account_information['valueChangePercentage'] / (account_information['totalValue'] / 100), 2)

    return account_information

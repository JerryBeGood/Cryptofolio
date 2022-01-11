import requests
import time
import datetime
import hmac
import hashlib


from cryptofolio.graphql_api.resolvers.shared_utilities import binance_exchange_info, binance_asset_ticker_info, validate_token, fetch_exchange_credentials
from cryptofolio import app

BINANCE_EXCHANGE_INFO = binance_exchange_info()
ASSET_TICKER_INFO = binance_asset_ticker_info()


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


def binance_account_info(authToken, recvWindow=5000):

    # Validate token
    token_validation_payload = validate_token(authToken)
    if not token_validation_payload[0]:
        return {'success': token_validation_payload[0], 'msg': token_validation_payload[1]}

    # Fetch exchange credentials
    exchange_credentials = fetch_exchange_credentials(
        token_validation_payload[1], 'binance')
    if not exchange_credentials[0]:
        return {'success': False, 'msg': exchange_credentials[1]}

    response_json = binance_account_info_request(
        exchange_credentials[1], exchange_credentials[2], recvWindow)

    account_information = binance_prepare_account_info_data(response_json)

    return {'success': True, 'msg': 'Ok', 'AccountInformation': account_information}


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
        order['time'] = datetime.datetime.utcfromtimestamp(
            int(position['time'])//1000)
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


def make_order(params, api_key):

    payload = {}

    with requests.post(f'{app.config.get("BINANCE")}/api/v3/order',
                       params=params,
                       headers={
                           'X-MBX-APIKEY': api_key,
                           'content-type': 'application/x-www-form-urlencoded'
                       }) as response:

        response_json = response.json()

        if response.status_code != 200:
            payload['success'] = False
            payload['code'] = response_json['code']
            payload['msg'] = response_json['msg']
        else:
            payload['success'] = True
            payload['status'] = response_json['status']

    return payload


def prepare_stop_loss_order_request_body(order, timestamp):
    request_body = ''
    if 'icebergQty' in order.keys():
        request_body = f'symbol={order["symbol"]}&side={order["side"]}&type=STOP_LOSS_LIMIT&icebergQty={order["icebergQty"]}&quantity={order["quantity"]}&timeInForce={order["timeInForce"]}&price={order["price"]}&stopPrice={order["stopPrice"]}&newOrderRespType=RESULT&timestamp={timestamp}'
    else:
        request_body = f'symbol={order["symbol"]}&side={order["side"]}&type=STOP_LOSS_LIMIT&quantity={order["quantity"]}&timeInForce={order["timeInForce"]}&price={order["price"]}&stopPrice={order["stopPrice"]}&newOrderRespType=RESULT&timestamp={timestamp}'

    return request_body


def prepare_stop_loss_order_params(order, timestamp):
    params = {}

    params['symbol'] = order["symbol"]
    params['side'] = order["side"]
    params['type'] = 'STOP_LOSS_LIMIT'
    params['quantity'] = order['quantity']
    params['timeInForce'] = order['timeInForce']
    params['price'] = order['price']
    params['stopPrice'] = order['stopPrice']
    params['newOrderRespType'] = 'RESULT'

    if 'icebergQty' in order.keys():
        params['icebergQty'] = order['icebergQty']

    params['timestamp'] = timestamp

    return params


def prepare_spot_market_order_request_body(order, timestamp):

    request_body = ''

    if order['base'] is True:
        request_body = f'symbol={order["symbol"]}&side={order["side"]}&type=MARKET&quantity={order["quantity"]}&timestamp={timestamp}'
    else:
        request_body = f'symbol={order["symbol"]}&side={order["side"]}&type=MARKET&quoteOrderQty={order["quantity"]}&timestamp={timestamp}'

    return request_body


def prepare_spot_market_order_params(order, timestamp):

    params = {
        'symbol': order["symbol"],
        'side': order['side'],
        'type': 'MARKET',
    }

    if order['base'] is True:
        params['quantity'] = order['quantity']
    else:
        params['quoteOrderQty'] = order['quantity']

    params['timestamp'] = timestamp

    return params


def prepare_spot_market_limit_order_params(order, timestamp):

    params = {}

    params['symbol'] = order["symbol"]
    params['side'] = order["side"]
    params['type'] = 'LIMIT'

    if 'icebergQty' in order.keys():
        params['icebergQty'] = order['icebergQty']

    params['quantity'] = order['quantity']
    params['timeInForce'] = order['timeInForce'] if 'timeInForce' in order.keys(
    ) else 'GTC'
    params['price'] = order['price']
    params['timestamp'] = timestamp

    return params


def prepare_spot_market_limit_order_request_body(order, timestamp):

    request_body = ''
    timeInForce = order['timeInForce'] if 'timeInForce' in order.keys(
    ) else 'GTC'

    if 'icebergQty' in order.keys():
        request_body = f'symbol={order["symbol"]}&side={order["side"]}&type=LIMIT&icebergQty={order["icebergQty"]}&quantity={order["quantity"]}&timeInForce={timeInForce}&price={order["price"]}&timestamp={timestamp}'
    else:
        request_body = f'symbol={order["symbol"]}&side={order["side"]}&type=LIMIT&quantity={order["quantity"]}&timeInForce={timeInForce}&price={order["price"]}&timestamp={timestamp}'

    return request_body


def binance_account_info_request(API_key, secret, recvWindow):
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

        return response.json()


def binance_prepare_account_info_data(response_json):
    account_information = {}
    account_information['totalValue'] = 0.0
    account_information['valueChangePercentage'] = 0.0
    account_information['balances'] = []

    for asset in response_json['balances']:
        balance = {}
        balance['asset'] = asset['asset']
        balance['value'] = round(float(asset['free']), 3)

        if asset['asset'] in ['USDT', 'BUSD']:
            balance['percentage'] = float(asset['free'])
            account_information['totalValue'] += balance['percentage']
        else:
            if f'{asset["asset"]}USDT' in ASSET_TICKER_INFO.keys():
                balance['percentage'] = float(
                    ASSET_TICKER_INFO[f'{asset["asset"]}USDT']
                    ['price']) * float(asset['free'])
            else:
                balance['percentage'] = None

            account_information['totalValue'] += balance['percentage']

        account_information['balances'].append(balance)

    for asset in account_information['balances']:
        if asset['asset'] not in ['USDT', 'BUSD']:
            account_information['valueChangePercentage'] += float(
                ASSET_TICKER_INFO[f'{asset["asset"]}USDT']
                ['priceChangePercent']) * (asset['percentage'] / 100)
        asset['percentage'] = round(
            asset['percentage'] / (account_information['totalValue'] / 100), 3)

    account_information['totalValue'] = round(
        account_information['totalValue'], 2)
    account_information['valueChangePercentage'] = round(
        account_information['valueChangePercentage'] / (account_information['totalValue'] / 100), 3)

    return account_information

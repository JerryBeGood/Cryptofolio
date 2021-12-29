import requests
import time
import hmac
import hashlib

from .utility_resolvers import ASSET_TICKER_INFO


def make_order(params, api_key):

    payload = {}

    with requests.post('https://testnet.binance.vision/api/v3/order',
                       params=params,
                       headers={
                           'X-MBX-APIKEY': api_key,
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

    print(request_body)
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
    params['timeInForce'] = order['timeInForce']
    params['price'] = order['price']
    params['timestamp'] = timestamp

    return params


def prepare_spot_market_limit_order_request_body(order, timestamp):

    request_body = ''

    if 'icebergQty' in order.keys():
        request_body = f'symbol={order["symbol"]}&side={order["side"]}&type=LIMIT&icebergQty={order["icebergQty"]}&quantity={order["quantity"]}&timeInForce={order["timeInForce"]}&price={order["price"]}&timestamp={timestamp}'
    else:
        request_body = f'symbol={order["symbol"]}&side={order["side"]}&type=LIMIT&quantity={order["quantity"]}&timeInForce={order["timeInForce"]}&price={order["price"]}&timestamp={timestamp}'

    return request_body


def binance_account_info_request(API_key, secret, recvWindow):
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

        return response.json()


def binance_prepare_account_info_data(response_json):
    account_information = {}
    account_information['totalValue'] = 0.0
    account_information['valueChangePercentage'] = 0.0
    account_information['balances'] = []

    for asset in response_json['balances']:
        balance = {}
        balance['asset'] = asset['asset']

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
            asset['percentage'] / (account_information['totalValue'] / 100), 2)

    account_information['totalValue'] = round(
        account_information['totalValue'], 2)
    account_information['valueChangePercentage'] = round(
        account_information['valueChangePercentage'] / (account_information['totalValue'] / 100), 2)

    return account_information

import requests


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

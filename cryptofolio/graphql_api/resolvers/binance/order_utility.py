
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

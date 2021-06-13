import requests
import time
import hmac, hashlib


def test_account_data_resolver(API_key, secret, recvWindow=5000):

    payload = {}

    timestamp = int(round(time.time() * 1000))
    request_body = f'timestamp={timestamp}'
    signature = hmac.new(secret.encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()

    with requests.get(f'https://testnet.binance.vision/api/v3/account',
                      params={
                          'timestamp': timestamp,
                          'signature': signature
                      },
                      headers={'X-MBX-APIKEY': API_key}) as response:

        print(response.json())


def test_open_orders_resolver(API_key, secret):

    timestamp = int(round(time.time() * 1000))
    request_body = f'timestamp={timestamp}'
    signature = hmac.new(secret.encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()

    with requests.get('https://testnet.binance.vision/api/v3/openOrders',
                      params={
                          'timestamp': timestamp,
                          'signature': signature
                      },
                      headers={'X-MBX-APIKEY': API_key}) as response:

        print(response.text)


def test_market_order(API_key, secret):

    timestamp = int(round(time.time() * 1000))
    request_body = f'symbol=LTCUSDT&side=BUY&type=MARKET&quantity=10.0&timestamp={timestamp}'
    signature = hmac.new(secret.encode(),
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()

    with requests.post('https://testnet.binance.vision/api/v3/order',
                       params={
                           'symbol': 'LTCUSDT',
                           'side': 'BUY',
                           'type': 'MARKET',
                           'quantity': 0.25,
                           'timestamp': timestamp,
                           'signature': signature
                       },
                       headers={
                           'X-MBX-APIKEY': API_key,
                           'content-type': 'application/x-www-form-urlencoded'
                       }) as response:

        print(response.json())


def exchange_info():

    payload = {}

    with requests.get(
            'https://testnet.binance.vision/api/v3/exchangeInfo') as response:

        response_json = response.json()

        for pair in response_json['symbols']:
            payload[pair['symbol']] = pair

    return payload


if __name__ == "__main__":
    # API_key = 'QvOlPyPcDcxrzFGIgG11qjIPsZMWgrU7dmNqw2Ifgcg3dKRXixUmAmSyEgo5P0LB'
    # secret = 'zhnhcx8tTgFOth5riTN35UG1McjzqQ4WhQQXbkeouxwlEr2jMU8uzMULyl1gmf5o'
    # #test_market_order(API_key, secret)
    # test_account_data_resolver(API_key, secret)
    # test_open_orders_resolver(API_key, secret)
    print(exchange_info())

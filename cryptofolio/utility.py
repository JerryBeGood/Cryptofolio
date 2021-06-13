import requests


def exchange_info():

    payload = {}

    with requests.get(
            'https://testnet.binance.vision/api/v3/exchangeInfo') as response:

        response_json = response.json()

        for pair in response_json['symbols']:
            payload[pair['symbol']] = pair

    return payload


EXCHANGE_INFO = exchange_info()
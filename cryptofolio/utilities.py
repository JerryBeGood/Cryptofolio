import requests


def exchange_info():

    payload = {}

    with requests.get(
            'https://testnet.binance.vision/api/v3/exchangeInfo') as response:

        response_json = response.json()

        for pair in response_json['symbols']:
            payload[pair['symbol']] = pair

    return payload


def asset_ticker_info():

    payload = {}

    with requests.get(
            'https://testnet.binance.vision/api/v3/ticker/24hr') as response:

        response_json = response.json()

        for pair in response_json:
            payload[pair['symbol']] = {
                'symbol': pair['symbol'],
                'priceChange': pair['priceChange'],
                'priceChangePercent': pair['priceChangePercent'],
                'price': pair['weightedAvgPrice']
            }

    return payload


EXCHANGE_INFO = exchange_info()
ASSET_TICKER_INFO = asset_ticker_info()
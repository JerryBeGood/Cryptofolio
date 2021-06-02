import requests as r
import json

with r.get('https://api.binance.com/api/v3/exchangeInfo') as response:

    payload = {}
    response_json = response.json()

    for asset_pair in response_json["symbols"]:
        symbol = {}
        symbol['status'] = asset_pair["status"]
        symbol['baseAsset'] = asset_pair['baseAsset']
        symbol['quoteAsset'] = asset_pair['quoteAsset']
        symbol['orderTypes'] = asset_pair['orderTypes']
        symbol['filters'] = asset_pair['filters']
        symbol['permissions'] = asset_pair['permissions']

        payload[asset_pair['symbol']] = symbol
        count = count + 1

    # for key, value in response.headers.items():
    #     print(f'{key}: {value}')

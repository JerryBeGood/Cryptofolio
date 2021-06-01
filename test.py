import requests as r
import json

with r.get('https://api.binance.com/api/v3/exchangeInfo',
           params={'symbol': 'BNBBTC'}) as response:

    for key, value in response.headers.items():
        print(f'{key}: {value}')

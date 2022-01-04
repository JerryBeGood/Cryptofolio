import time
import requests
import hmac
import hashlib


def validate_bybit_credentials(API_key, secret):

    timestamp = int(round(time.time() * 1000))
    request_body = f'api_key={API_key}&timestamp={timestamp}'
    sign = hmac.new(secret.encode(),
                    request_body.encode('UTF-8'),
                    digestmod=hashlib.sha256).hexdigest()

    with requests.get(f'https://api-testnet.bybit.com/spot/v1/account',
                      params={
                          'api_key': API_key,
                          'timestamp': timestamp,
                          'sign': sign
                      }) as response:

        if response.status_code == 200:
            return True, response
        else:
            return False, response

# recvWindow = 5000
#     timestamp = int(round(time.time() * 1000))
#     request_body = f'recvWindow={recvWindow}&timestamp={timestamp}'
#     signature = hmac.new(secret.encode(),
#                          request_body.encode('UTF-8'),
#                          digestmod=hashlib.sha256).hexdigest()

#     with requests.get(f'https://testnet.binance.vision/api/v3/account',
#                       params={
#                           'recvWindow': recvWindow,
#                           'timestamp': timestamp,
#                           'signature': signature
#                       },
#                       headers={'X-MBX-APIKEY': API_key}) as response:

#         if response.status_code == 200:
#             return True, response
#         else:
#             return False, response

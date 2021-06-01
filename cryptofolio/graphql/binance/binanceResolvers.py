import requests
import time
import hmac, hashlib


# binanceAccountData query resolver
def resolve_binanceAccountData(obj, info, API_key, secret, recvWindow=5000):

    payload = []

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

        response_json = response.json()

        binanceAccount = {}
        binanceAccount['totalWalletBalance'] = response_json[
            'totalWalletBalance']
        binanceAccount['availableBalance'] = response_json['availableBalance']

        payload = binanceAccount

    return payload
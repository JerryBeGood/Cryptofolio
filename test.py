import requests
import time
import hmac, hashlib


def getAccountInfo():

    recvWindow = 50000
    timestamp = int(round(time.time() * 1000))
    API_key = '39c85920508f517f7f012307f5b06472226d37a51254afc3e1342f17bd890e01'
    secret = b'81a51dd0d3f254de481baf5d41daf2a9b41ec5a68f4fdff79cc4b355c1eb665a'

    request_body = f'recvWindow={recvWindow}&timestamp={timestamp}'

    signature = hmac.new(secret,
                         request_body.encode('UTF-8'),
                         digestmod=hashlib.sha256).hexdigest()

    print(f'timestamp: {timestamp}')
    print(f'signature: {signature}')

    with requests.get(f'https://testnet.binancefuture.com/fapi/v1/account',
                      params={
                          'recvWindow': recvWindow,
                          'timestamp': timestamp,
                          'signature': signature
                      },
                      headers={'X-MBX-APIKEY': API_key}) as response:

        print(response.json()['totalWalletBalance'])


getAccountInfo()
import requests
import time
import hmac
import hashlib

from cryptofolio.utilities import EXCHANGE_INFO, ASSET_TICKER_INFO, validate_token, fetch_exchange_credentials


def binance_account_info_resolver(obj, info, authToken, recvWindow=5000):

    # Validate token
    token_validation_payload = validate_token(authToken)
    print(token_validation_payload)
    if not token_validation_payload[0]:
        return {'success': token_validation_payload[0], 'msg': token_validation_payload[1]}

    # Fetch exchange credentials
    exchange_credentials = fetch_exchange_credentials(
        token_validation_payload[1], 'binance')
    print(exchange_credentials)
    if not exchange_credentials[0]:
        return {'success': False, 'msg': exchange_credentials[1]}

    response_json = binance_account_info_request(
        exchange_credentials[1], exchange_credentials[2], recvWindow)

    account_information = binance_prepare_account_info_data(response_json)

    return {'success': True, 'msg': 'Ok', 'AccountInformation': account_information}


def binance_exchange_info_resolver(obj, info, symbols=None):

    keys = EXCHANGE_INFO.keys()
    payload = []

    if symbols is None:
        payload = EXCHANGE_INFO.values()
    else:
        for symbol in symbols:
            if symbol in keys:
                payload.append(EXCHANGE_INFO[symbol])

    return payload


def binance_account_info_request(API_key, secret, recvWindow):
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

        return response.json()


def binance_prepare_account_info_data(response_json):
    account_information = {}
    account_information['totalValue'] = 0.0
    account_information['valueChangePercentage'] = 0.0
    account_information['balances'] = []

    for asset in response_json['balances']:
        balance = {}
        balance['asset'] = asset['asset']

        if asset['asset'] in ['USDT', 'BUSD']:
            balance['percentage'] = float(asset['free'])
            account_information['totalValue'] += balance['percentage']
        else:
            if f'{asset["asset"]}USDT' in ASSET_TICKER_INFO.keys():
                balance['percentage'] = float(
                    ASSET_TICKER_INFO[f'{asset["asset"]}USDT']
                    ['price']) * float(asset['free'])
            else:
                balance['percentage'] = None

            account_information['totalValue'] += balance['percentage']

        account_information['balances'].append(balance)

    for asset in account_information['balances']:
        if asset['asset'] not in ['USDT', 'BUSD']:
            account_information['valueChangePercentage'] += float(
                ASSET_TICKER_INFO[f'{asset["asset"]}USDT']
                ['priceChangePercent']) * (asset['percentage'] / 100)
        asset['percentage'] = round(
            asset['percentage'] / (account_information['totalValue'] / 100), 2)

    account_information['totalValue'] = round(
        account_information['totalValue'], 2)
    account_information['valueChangePercentage'] = round(
        account_information['valueChangePercentage'] / (account_information['totalValue'] / 100), 2)

    return account_information

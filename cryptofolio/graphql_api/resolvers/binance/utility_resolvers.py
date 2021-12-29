from cryptofolio.graphql_api.resolvers.shared_utilities import validate_token, fetch_exchange_credentials, binance_exchange_info, binance_asset_ticker_info

EXCHANGE_INFO = binance_exchange_info()
ASSET_TICKER_INFO = binance_asset_ticker_info()


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

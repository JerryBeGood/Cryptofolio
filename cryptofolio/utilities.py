import requests
import jwt

from cryptography.fernet import Fernet

from cryptofolio import app
from cryptofolio.models import Exchange


def fetch_exchange_credentials(token_claims, exchange):

    exchange_credentials = Exchange.query.filter_by(
        user_id=token_claims['iss']).filter_by(exchange=exchange).first()
    print(exchange_credentials)
    if not exchange_credentials:
        return False, f"{exchange} credentials doesn't exist for this account"

    try:
        cipher_suite = Fernet(app.config.get('EXCHANGE_SECRET_KEY'))
        API_key = cipher_suite.decrypt(
            exchange_credentials.api_key).decode('UTF-8')
        secret = cipher_suite.decrypt(
            exchange_credentials.secret).decode('UTF-8')
    except Exception as error:
        print(str(error))
        return False, 'Decryption error'
    else:
        return True, API_key, secret


def exchange_info():

    payload = {}

    with requests.get(
            'https://api1.binance.com/api/v3/exchangeInfo') as response:

        response_json = response.json()

        for pair in response_json['symbols']:
            payload[pair['symbol']] = pair

    return payload


def asset_ticker_info():

    payload = {}

    with requests.get(
            'https://api1.binance.com/api/v3/ticker/24hr') as response:

        response_json = response.json()

        for pair in response_json:
            payload[pair['symbol']] = {
                'symbol': pair['symbol'],
                'priceChange': pair['priceChange'],
                'priceChangePercent': pair['priceChangePercent'],
                'price': pair['weightedAvgPrice']
            }

    return payload


def validate_token(authToken):
    try:
        jwt_claims = jwt.decode(
            jwt=authToken,
            key=app.config.get('SECRET_KEY'),
            algorithms=['HS256'],
            options={
                'verify_signature': True,
                'require': ['exp', 'iat', 'iss'],
                'verify_exp': True,
                'verify_iat': True
            }
        )
    except jwt.exceptions.InvalidTokenError as error:
        return False, str(error)
    except jwt.exceptions.DecodeError as error:
        return False, str(error)
    except jwt.exceptions.ExpiredSignatureError as error:
        return False, str(error)
    except jwt.exceptions.InvalidIssuedAtError as error:
        return False, str(error)
    except jwt.exceptions.InvalidKeyError as error:
        return False, str(error)
    except jwt.exceptions.InvalidAlgorithmError as error:
        return False, str(error)
    except jwt.exceptions.MissingRequiredClaimError as error:
        return False, str(error)
    else:
        return True, jwt_claims


EXCHANGE_INFO = exchange_info()
ASSET_TICKER_INFO = asset_ticker_info()

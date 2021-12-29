import requests
import time, datetime
import hmac, hashlib
import jwt

from cryptofolio import app, db
from cryptofolio.models import Code


def validate_exchange_credentials(API_key, secret, exchange):

    if exchange == 'binance':
        recvWindow = 5000
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

            if response.status_code == 200:
                return True, response
            else:
                return False, response
    else:
        return False, 'ByBit not yet implemented'


def generate_auth_token(user):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=60),
            'iat': datetime.datetime.utcnow(),
            'iss': user.id,
        }
        return True, jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return False, e


def code_auth(user, type, code):
    the_code = Code.query.filter_by(code=code).filter_by(
        user_id=user.id).filter_by(type=type).first()
    if not the_code:
        False, f'Wrong {type} code'
    elif the_code.timestamp - int(datetime.datetime.utcnow().timestamp()) < -300000:
        db.session.delete(the_code)
        db.session.commit()
        return False, f'{type} code overdue'
    else:
        db.session.delete(the_code)
        db.session.commit()
        return True, 'Ok'

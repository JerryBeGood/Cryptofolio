import datetime
import jwt

from cryptofolio import app, db
from cryptofolio.graphql_api.resolvers.binance import validate_binance_credentials
from cryptofolio.graphql_api.resolvers.bybit.utility import validate_bybit_credentials
from cryptofolio.models import Code


def validate_exchange_credentials(API_key, secret, exchange):

    if exchange == 'binance':
        return validate_binance_credentials(API_key, secret)
    elif exchange == 'bybit':
        return validate_bybit_credentials(API_key, secret)


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

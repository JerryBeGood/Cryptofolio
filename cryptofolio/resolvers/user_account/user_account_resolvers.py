import secrets

import datetime

from .user_account_utility import validate_exchange_credentials, generate_auth_token, code_auth
from cryptofolio.resolvers.shared_utilities import validate_token

from flask_mail import Message
from cryptography.fernet import Fernet

from cryptofolio.models import User, db, Exchange, Code
from cryptofolio import bcrypt, mail, app


def sign_up_resolver(obj, info, email, password):

    if User.query.filter_by(email=email).first():
        return {'Success': False, 'Token': 'Account already exists'}

    user = User(**{
        'email': email,
        'password': bcrypt.generate_password_hash(password).decode('utf-8')
    })
    db.session.add(user)
    db.session.flush()

    activation_code = Code(**{
        'user_id': user.id,
        'type': 'activation',
        'code': secrets.choice(range(10001, 99999)),
    })
    db.session.add(activation_code)

    try:
        db.session.commit()
    except Exception as error:
        print(str(error))
        return {'Success': True, 'Token': 'Database error'}

    try:
        msg = Message(
            'Cryptofolio - activation code',
            recipients=[user.email],
            body=f'{activation_code.code}',
            sender=("Cryptofolio", 'cryptofolio.service@gmail.com')
        )
        mail.send(msg)
    except Exception as error:
        db.session.delete(user)
        db.session.delete(activation_code)
        db.session.commit()
        print(str(error))
        return {'Success': False, 'Token': 'Activation mail error'}

    return {'Success': True, 'Token': 'Activation email sent'}


def activate_account_resolver(obj, info, email, password, code):

    user = User.query.filter_by(email=email).first()

    if not user:
        return {'Success': False, 'Token': "Account doesn't exist"}

    if not bcrypt.check_password_hash(user.password, password):
        return {'Success': False, 'Token': 'Wrong password'}

    if user.is_activated:
        return {'Success': False, 'Token': 'Account already activated'}

    code_validation = code_auth(user, 'activation', code)
    if not code_validation[0]:
        return {'Success': code_validation[0], 'Token': code_validation[1]}

    try:
        user.is_activated = True
        db.session.commit()
    except Exception as error:
        print(str(error))
        return {'Success': False, 'Token': 'Database error'}

    auth_token = generate_auth_token(user)

    return {'Success': auth_token[0], 'Token': auth_token[1]}


def generate_activation_code_resolver(obj, info, email, password):
    user = User.query.filter_by(email=email).first()

    if not user:
        return {'Success': False, 'Token': "Account doesn't exist"}

    if not bcrypt.check_password_hash(user.password, password):
        return {'Success': False, 'Token': 'Wrong password'}

    if user.is_activated:
        return {'Success': False, 'Token': 'Account already activated'}

    activation_code = Code.query.filter_by(
        user_id=user.id).filter_by(type='activation').first()
    if activation_code:
        db.session.delete(activation_code)

    activation_code = {
        'user_id': user.id,
        'type': 'activation',
        'code': secrets.choice(range(10001, 99999)),
        'timestamp': int(datetime.datetime.utcnow().timestamp()),
    }

    try:
        db.session.add(Code(**activation_code))
        db.session.commit()
    except Exception as error:
        print(str(error))
        return {'Success': False, 'Token': 'Database error'}

    try:
        msg = Message(
            'Cryptofolio - activation code',
            recipients=[email],
            body=f'{activation_code}',
            sender=("Cryptofolio", 'cryptofolio.service@gmail.com')
        )
        mail.send(msg)
    except Exception as error:
        return {'Success': False, 'Token': error}

    return {'Success': True, 'Token': 'Activation email sent'}


def sign_in_resolver(obj, info, email, password):
    user = User.query.filter_by(email=email).first()

    if not user:
        return {'Success': False, 'Token': "Account doesn't exist"}

    if not bcrypt.check_password_hash(user.password, password):
        return {'Success': False, 'Token': 'Wrong password'}

    if not user.is_activated:
        return {'Success': False, 'Token': 'Account not yet activated'}

    auth_token = generate_auth_token(user)

    return {'Success': auth_token[0], 'Token': auth_token[1]}


def account_status_resolver(obj, info, authToken):

    validation_payload = validate_token(authToken)

    if not validation_payload[0]:
        return {'Success': validation_payload[0], 'Token': validation_payload[1]}

    user = User.query.filter_by(id=validation_payload[1]['iss']).first()

    return {'email': user.email, 'binance': user.binance, 'bybit': user.bybit}


def add_exchange_resolver(obj, info, API_key, secret, authToken, exchange):

    token_validation_payload = validate_token(authToken)
    if not token_validation_payload[0]:
        return {'Success': token_validation_payload[0], 'Token': token_validation_payload[1]}

    exchange_validation_payload = validate_exchange_credentials(
        API_key, secret, exchange)
    if not exchange_validation_payload[0]:
        return {'Success': exchange_validation_payload[0], 'Token': 'Exchange credentials not valid'}

    user = User.query.filter_by(id=token_validation_payload[1]['iss']).first()

    if exchange == 'binance':
        if user.binance is True:
            return {'Success': False, 'Token': 'Exchange credetnials already exist'}
        else:
            user.binance = True
    elif exchange == 'bybit':
        if user.bybit is True:
            return {'Success': False, 'Token': 'Exchange credetnials already exist'}
        else:
            user.bybit = True

    cipher_suite = Fernet(app.config.get('EXCHANGE_SECRET_KEY'))

    new_exchange = {
        'user_id': user.id,
        'exchange': exchange,
        'api_key': cipher_suite.encrypt(str.encode(API_key)),
        'secret': cipher_suite.encrypt(str.encode(secret))
    }

    try:
        db.session.add(Exchange(**new_exchange))
        db.session.commit()
    except Exception as error:
        print(str(error))
        return {'Success': False, 'Token': 'Database error'}

    return {'Success': True, 'Token': 'Exchange added to the account'}


def generate_pswd_recovery_code_resolver(obj, info, email):

    # Check whether email adress exists in db
    user = User.query.filter_by(email=email).first()

    if not user:
        return {'Success': False, 'Token': "Account doesn't exist"}

    # Generate recovery code
    recovery_code = Code.query.filter_by(
        user_id=user.id).filter_by(type='recovery').first()
    if recovery_code:
        try:
            db.session.delete(recovery_code)
            db.session.commit()
        except Exception as error:
            print(str(error))
            return {'Success': False, 'Token': 'Database error'}

    recovery_code = {
        "user_id": user.id,
        "type": "recovery",
        "code": secrets.choice(range(10001, 99999)),
        "timestamp": int(datetime.datetime.utcnow().timestamp())
    }

    # Save it to db
    try:
        db.session.add(Code(**recovery_code))
        db.session.commit()
    except Exception as error:
        print(str(error))
        return {'Success': False, 'Token': 'Database error'}

    # Send it to user
    try:
        msg = Message(
            'Cryptofolio - password recovery code',
            recipients=[user.email],
            body=f'{recovery_code["code"]}',
            sender=("Cryptofolio", 'cryptofolio.service@gmail.com')
        )
        mail.send(msg)
    except Exception as error:
        return {'Success': False, 'Token': error}

    # Respond to app
    return {'Success': True, 'Token': 'Recovery code sent'}


def recover_password_resolver(obj, info, email, password, code):

    # Check whether email adress exists in db
    user = User.query.filter_by(email=email).first()
    if not user:
        return {'Success': False, 'Token': "Account doesn't exist"}

    # Validate code & delete it
    recovery_code = Code.query.filter_by(code=code).filter_by(
        user_id=user.id).filter_by(type='recovery').first()
    if not recovery_code:
        return {'Success': False, 'Token': 'Wrong recovery code'}
    elif recovery_code.timestamp - int(datetime.datetime.utcnow().timestamp()) < -300000:
        db.session.delete(recovery_code)
        db.session.commit()
        return {'Success': False, 'Token': 'Recovery code overdue'}

    # Save new password to db
    try:
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        db.session.delete(recovery_code)
        db.session.commit()
    except Exception as error:
        print(str(error))
        return {'Success': False, 'Token': 'Database error'}

    # Send confimration
    return {'Success': True, 'Token': 'Password changed'}


def delete_account_resolver(obj, info, authToken):

    validation_payload = validate_token(authToken)
    if not validation_payload[0]:
        return {'Success': validation_payload[0], 'Token': validation_payload[1]}

    user = User.query.filter_by(id=validation_payload[1]['iss']).first()
    if not user:
        return {'Success': False, 'Token': "Account doesn't exist"}

    try:
        Code.query.filter_by(user_id=user.id).delete()
        Exchange.query.filter_by(user_id=user.id).delete()
        db.session.delete(user)
        db.session.commit()
    except Exception as error:
        print(str(error))
        return {'Success': False, 'Token': 'Database error'}

    return {'Success': True, 'Token': 'Account deleted'}


def change_password_resolver(obj, info, authToken, password):

    # validate jwt
    validation_payload = validate_token(authToken)
    if not validation_payload[0]:
        return {'Success': validation_payload[0], 'Token': validation_payload[1]}

    try:
        user = User.query.filter_by(id=validation_payload[1]['iss']).first()
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        db.session.commit()
    except Exception as error:
        print(str(error))
        return {'Success': False, 'Token': 'Database error'}
    
    return {'Success': True, 'Token': 'Password changed'}


def delete_exchange_resolver(obj, info, authToken, exchange):

    # validate jwt
    token_validation_payload = validate_token(authToken)
    if not token_validation_payload[0]:
        return {'Success': token_validation_payload[0], 'Token': token_validation_payload[1]}

    # validate existance of a exchange
    user = User.query.filter_by(id=token_validation_payload[1]['iss']).first()
    exchange = Exchange.query.filter_by(
        user_id=user.id).filter_by(exchange=exchange).first()
    if not exchange:
        return {'Success': False, 'Token': "No such exchange connected to the account"}

    # delete exchange
    try:
        if exchange.exchange == 'binance':
            user.binance = False
        elif exchange.exchange == 'bybit':
            user.bybit = False
        db.session.delete(exchange)
        db.session.commit()
    except Exception as error:
        print(str(error))
        return {'Success': False, 'Token': 'Database error'}

    # return status
    return {'Success': True, 'Token': 'Exchange deleted successfully'}

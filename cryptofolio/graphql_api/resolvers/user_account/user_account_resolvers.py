import secrets
import jwt
import datetime
from flask_mail import Message

from cryptofolio.models import User, db
from cryptofolio import bcrypt, mail, app


def sign_up_resolver(obj, info, email, password):

    if User.query.filter_by(email=email).first():
        return {'Success': False, 'Token': 'Account already exists'}

    new_user = {
        'email': email,
        'password': bcrypt.generate_password_hash(password).decode('utf-8'),
        'is_activated': False,
        'activation_code': secrets.randbelow(99999),
        'binance': False,
        'bybit': False
    }

    try:
        msg = Message(
            'Cryptofolio - activation code',
            recipients=[new_user['email']],
            body=f'{new_user["activation_code"]}',
            sender=("Cryptofolio", 'cryptofolio.service@gmail.com')
        )
        mail.send(msg)
    except Exception as error:
        return {'Success': False, 'Token': error}

    db.session.add(User(**new_user))
    db.session.commit()

    return {'Success': True, 'Token': 'Activation email sent'}


def activate_account_resolver(obj, info, email, password, code):

    user = User.query.filter_by(email=email).first()

    if not user:
        return {'Success': False, 'Token': "Account doesn't exist"}

    if not bcrypt.check_password_hash(user.password, password):
        return {'Success': False, 'Token': 'Wrong password'}

    if user.is_activated:
        return {'Success': False, 'Token': 'Account already activated'}

    if user.activation_code != code:
        return {'Success': False, 'Token': 'Wrong activation code'}

    user.is_activated = True
    db.session.commit()

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

    activation_code = secrets.randbelow(99999)

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

    user.activation_code = activation_code
    db.session.commit()
    
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
        return False, error
    except jwt.exceptions.DecodeError as error:
        return False, error
    except jwt.exceptions.ExpiredSignatureError as error:
        return False, error
    except jwt.exceptions.InvalidIssuedAtError as error:
        return False, error
    except jwt.exceptions.InvalidKeyError as error:
        return False, error
    except jwt.exceptions.InvalidAlgorithmError as error:
        return False, error
    except jwt.exceptions.MissingRequiredClaimError as error:
        return False, error
    else:
        return True, jwt_claims


def generate_auth_token(user):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
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
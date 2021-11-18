import secrets
from flask_mail import Message

from cryptofolio.models import User, db
from cryptofolio import bcrypt, mail


def sign_up_resolver(obj, info, email, password):

    # Check whether such email exists in db
    if User.query.filter_by(email=email).first():
        return {'Success': False, 'Token': 'Already used email'}

    # Save new user to db
    new_user = {
        'email': email,
        'password': bcrypt.generate_password_hash(password).decode('utf-8'),
        'is_activated': False,
        'activation_code': secrets.randbelow(99999)
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

    # db.session.add(User(**new_user))
    # db.session.commit()

    return {'Success': True, 'Token': 'Activation email sent'}

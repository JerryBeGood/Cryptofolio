class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = b'sqn\xd1\x9dH!\x92\xd4\x99\xfd\xf2\xd2r`S\xa4n\xfbt\xb7E\xfc\xa2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:admin1@localhost:5432/cryptofolio'

    """flask_mail configuration"""
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'cryptofolio.service@gmail.com'
    MAIL_PASSWORD = 'Cryptofolio1'


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True

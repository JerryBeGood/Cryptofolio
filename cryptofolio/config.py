class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
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

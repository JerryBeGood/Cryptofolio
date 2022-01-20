"""Base configuration"""
DEBUG = False
TESTING = False
SECRET_KEY = b''
EXCHANGE_SECRET_KEY = b''
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = ''

"""flask_mail configuration"""
MAIL_SERVER = ''
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = ''
MAIL_PASSWORD = ''

# """Exchanges urls"""
BINANCE = 'https://api.binance.com'
BYBIT = 'https://api.bybit.com'

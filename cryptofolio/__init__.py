from cryptofolio.utility import fetch_binance_exchange_info_data
from flask import Flask

#Application
app = Flask(__name__.split('.')[0])

binance_exchange_info = fetch_binance_exchange_info_data()

from cryptofolio import routes

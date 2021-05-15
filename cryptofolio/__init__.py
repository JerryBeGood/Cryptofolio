from flask import Flask

#Application
app = Flask(__name__.split('.')[0])

from cryptofolio import routes

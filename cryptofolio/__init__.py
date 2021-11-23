from flask import Flask
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_mail import Mail

from cryptofolio.models import db
from cryptofolio.config import DevelopmentConfig

app = Flask(__name__.split('.')[0])
app.config.from_object(DevelopmentConfig)

mail = Mail()
bcrypt = Bcrypt()

db.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)
app.app_context().push()

from cryptofolio import routes
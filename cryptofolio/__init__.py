from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail

from cryptofolio.models import db


app = Flask(__name__.split('.')[0])
app.config.from_pyfile('init_config.py')

mail = Mail()
bcrypt = Bcrypt()

db.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)
app.app_context().push()


from cryptofolio import routes

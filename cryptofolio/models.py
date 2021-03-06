from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)
    is_activated = db.Column(db.Boolean, nullable=False,
                             default=False)
    binance = db.Column(db.Boolean, nullable=False,
                        default=False)
    bybit = db.Column(db.Boolean, nullable=False, default=False)


class Exchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
    exchange = db.Column(db.String(10), nullable=False)
    api_key = db.Column(db.LargeBinary, unique=True, nullable=False)
    secret = db.Column(db.LargeBinary, unique=True, nullable=False)


class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    code = db.Column(db.String(5), nullable=False)
    timestamp = db.Column(db.BigInteger, nullable=False, default=int(
        datetime.utcnow().timestamp()))

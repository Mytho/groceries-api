import os
import jwt
import sqlalchemy as sa
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()


def init_models(app):
    db.init_app(app)


def decode_token(token):
    return jwt.decode(token, os.environ.get('JWT_SECRET'))


def encode_token(payload):
    return jwt.encode(payload, os.environ.get('JWT_SECRET'))


class Item(db.Model):

    __tablename__ = 'items'

    id = sa.Column('id', sa.Integer, primary_key=True)
    name = sa.Column('name', sa.String(255), nullable=False)
    is_bought = sa.Column('is_bought', sa.Boolean, default=False,
                          nullable=False)
    modified = sa.Column('modified', sa.DateTime, default=sa.func.now(),
                         onupdate=sa.func.now(), nullable=False)

    def as_dict(self):
        return dict(id=self.id, name=self.name, is_bought=self.is_bought)


class User(db.Model):

    __tablename__ = 'users'

    id = sa.Column('id', sa.Integer, primary_key=True)
    username = sa.Column('username', sa.String(128), nullable=False,
                         unique=True)
    password = sa.Column('password', sa.String(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    @staticmethod
    def by_token(token):
        payload = decode_token(token)
        return User.query.filter(User.id == payload.get('id')).first()

    @staticmethod
    def by_username(username):
        return User.query.filter(User.username == username).first()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def token(self):
        return encode_token({'id': self.id})

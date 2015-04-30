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


class User(db.Model):

    __tablename__ = 'users'

    id = sa.Column('id', sa.Integer, primary_key=True)
    username = sa.Column('username', sa.String(64), nullable=False,
                         unique=True)
    password = sa.Column('password', sa.String(64), nullable=False)

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

import sqlalchemy as sa
from flask.ext.sqlalchemy import SQLAlchemy

from application.auth import encode_token


db = SQLAlchemy()


def init_models(app):
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'

    id = sa.Column('id', sa.Integer, primary_key=True)
    username = sa.Column('username', sa.String(64), nullable=False,
                         unique=True)
    password = sa.Column('password', sa.String(64), nullable=False)

    @staticmethod
    def by_username(username):
        return User.query.filter(User.username == username).first()

    def token(self):
        return encode_token({'id': self.id})

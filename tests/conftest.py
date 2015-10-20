import os
import pytest

from alembic import command
from alembic.config import Config
from functools import partial

from application.core import make_app
from application.models import Item, User, db as _db, encode_token


os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['JWT_SECRET'] = 'A_VERY_SECRET_KEY'


@pytest.yield_fixture(scope='session')
def app():
    app = make_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': os.environ['DATABASE_URL'],
    })

    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture(scope='session')
def client(app):
    return TestClient(app)


@pytest.yield_fixture(scope='session')
def db(app):
    _db.app = app

    connection = _db.engine.connect()
    config = Config(os.path.abspath('alembic.ini'))
    config.attributes['connection'] = connection
    command.upgrade(config, 'head')

    yield _db

    connection.close()
    _db.drop_all()


@pytest.fixture(scope='function')
def items(db):
    db.session.add_all([
        Item(name='apple'),
        Item(name='banana'),
        Item(name='cucumber'),
        Item(name='dill'),
        Item(name='eggplant'),
    ])
    db.session.commit()

    return Item.query.all()


@pytest.fixture(scope='session')
def user(db):
    password = 'letmein'
    user = User(username='tester', password=password)
    user.plaintext_password = password

    db.session.add(user)
    db.session.commit()

    return user


class TestClient(object):

    def __init__(self, app):
        self.app = app

    def __getattr__(self, name):
        return partial(self._open, name)

    def _open(self, http_method, url, headers=None, data=None, user=None,
              assert_status_code=200, assert_headers=None):

        if headers is None:
            headers = {'Content-Type': 'application/json'}

        if user:
            headers['X-Auth-Token'] = encode_token(dict(id=user.id))

        client = self.app.test_client()
        method = getattr(client, http_method.lower())
        resp = method(url, headers=headers, data=data)

        assert resp.status_code == assert_status_code

        if assert_headers is not None:
            for key, val in assert_headers:
                assert resp.headers[key] == val

        return resp

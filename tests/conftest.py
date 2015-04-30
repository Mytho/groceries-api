import os
import pytest
from alembic import command
from alembic.config import Config

from application.core import make_app
from application.models import db as _db


os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['JWT_SECRET'] = 'A_VERY_SECRET_KEY'


@pytest.fixture(scope='session')
def app(request):
    app = make_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': os.environ['DATABASE_URL'],
    })

    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def db(app, request):
    _db.app = app

    connection = _db.engine.connect()
    config = Config(os.path.abspath('alembic.ini'))
    config.attributes['connection'] = connection
    command.upgrade(config, 'head')

    def teardown():
        connection.close()
        _db.drop_all()

    request.addfinalizer(teardown)
    return _db

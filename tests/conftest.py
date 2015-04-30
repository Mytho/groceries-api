import os
import pytest
from alembic.command import upgrade
from alembic.config import Config

from application.core import make_app
from application.models import db as _db


os.environ['DATABASE_URL'] = 'sqlite://'
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
    _db.create_all()
    upgrade(Config(os.path.abspath('alembic.ini')), 'head')

    def teardown():
        _db.drop_all()

    request.addfinalizer(teardown)
    return _db

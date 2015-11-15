import string
import random

import pytest

from radar_api.app import create_app
from radar.database import db


@pytest.fixture(scope='session')
def app():
    return create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgres://localhost:5432/radar_test',
        'SECRET_KEY': ''.join(random.sample(string.printable, 32)),
        'BASE_URL': 'http://localhost'
    })


@pytest.yield_fixture(scope='session')
def app_context(app):
    with app.app_context() as app_context:
        yield app_context


@pytest.fixture(scope='session')
def test_db(request, app_context):
    db.drop_all()
    db.create_all()

    def teardown():
        db.drop_all()

    request.addfinalizer(teardown)

    return db


@pytest.fixture
def transaction(request, app_context, test_db):
    db.session.begin_nested()

    def teardown():
        db.session.rollback()

    request.addfinalizer(teardown)

    return db


@pytest.yield_fixture
def client(app, app_context):
    with app.test_client() as client:
        yield client

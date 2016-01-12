import random
import string

import pytest

from radar.app import create_app
from radar.database import db
from radar.models.source_types import SourceType


@pytest.fixture(scope='session')
def app():
    return create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgres://postgres@localhost/radar_test',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': ''.join(random.sample(string.printable, 32)),
        'BASE_URL': 'http://localhost',
    })


@pytest.yield_fixture(scope='session')
def app_context(app):
    with app.app_context() as app_context:
        yield app_context


@pytest.fixture(scope='session', autouse=True)
def test_db(request, app_context):
    db.drop_all()
    db.create_all()

    db.session.add(SourceType(id='RADAR', name='RaDaR'))
    db.session.commit()

    def teardown():
        db.session.close()
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

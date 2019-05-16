import pytest

from radar.api.app import RadarAPI
from radar.database import db
from tests.api.client import TestClient
from tests.api.fixtures import create_fixtures


@pytest.yield_fixture(scope='session')
def api(app):
    app = RadarAPI({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgresql://radar:password@localhost/radar_test',
        'BASE_URL': 'http://localhost',
        'PASSWORD_HASH_METHOD': 'pbkdf2:sha1:1',
    })

    app.test_client_class = TestClient

    with app.app_context():
        yield app


@pytest.yield_fixture(scope='session')
def tables(api):
    db.drop_all()
    db.create_all()

    # Create fixtures here so the tests run faster
    # TODO should probably be changed so tests can have different fixtures
    create_fixtures()
    db.session.commit()

    yield db

    db.drop_all()


@pytest.yield_fixture(scope='function', autouse=True)
def session(api, tables):
    connection = db.engine.connect()
    transaction = connection.begin()
    session = db.create_scoped_session(options=dict(bind=connection, binds={}))
    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()

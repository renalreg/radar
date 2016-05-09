import pytest

from radar.api.app import RadarAPI
from radar.tests.api.client import TestClient


@pytest.yield_fixture(scope='session', autouse=True)
def app():
    app = RadarAPI({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgres://postgres@localhost/radar_test',
        'BASE_URL': 'http://localhost',
        'PASSWORD_HASH_METHOD': 'pbkdf2:sha1:1',
    })

    app.test_client_class = TestClient

    with app.app_context():
        yield app

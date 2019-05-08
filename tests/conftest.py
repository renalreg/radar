import pytest

from radar.app import Radar


@pytest.yield_fixture(scope='session', autouse=True)
def app():
    app = Radar({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgres://radar:password@localhost/radar_test',
        'BASE_URL': 'http://localhost',
        'PASSWORD_HASH_METHOD': 'pbkdf2:sha1:1',
    })

    with app.app_context():
        yield app

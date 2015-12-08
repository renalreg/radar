import random
import string

import pytest

from radar.app import create_app


@pytest.fixture(scope='session')
def app():
    return create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgres://postgres@localhost/radar_test',
        'SECRET_KEY': ''.join(random.sample(string.printable, 32)),
        'BASE_URL': 'http://localhost',
        'UKRDC_SEARCH_ENABLED': True,
        'UKRDC_SEARCH_URL': 'http://localhost:5101/search',
    })

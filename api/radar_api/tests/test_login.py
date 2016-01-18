import json

import pytest

from radar.database import db
from radar_api.tests.fixtures import create_user


def login(client, username, password):
    response = client.post(
        '/login',
        data={
            'username': username,
            'password': password
        }
    )

    return response


@pytest.fixture
def user():
    u = create_user('admin')
    db.session.commit()
    return u


def test_good_login(app, session, user):
    client = app.test_client()

    response = login(client, 'admin', 'password')

    assert response.status_code == 200

    data = json.loads(response.data)

    assert data['user_id'] == user.id
    assert 'token' in data


def test_bad_login(app, user):
    client = app.test_client()

    response = login(client, 'admin', 'foo')

    assert response.status_code == 422

    data = json.loads(response.data)

    assert data == {
        'errors': {
            'username': ['Incorrect username or password.']
        }
    }

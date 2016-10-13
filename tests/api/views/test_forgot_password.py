import json

from radar.database import db
from tests.api.fixtures import get_user


def test_forgot_password(api):
    user = get_user('admin')

    client = api.test_client()

    assert user.reset_password_token is None
    assert user.reset_password_date is None

    response = client.post('/forgot-password', data={
        'username': user.username,
        'email': user.email
    })

    assert response.status_code == 200

    db.session.refresh(user)

    assert user.reset_password_token is not None
    assert user.reset_password_date is not None


def test_missing_username(api):
    user = get_user('admin')

    client = api.test_client()

    response = client.post('/forgot-password', data={
        'email': user.email,
    })

    assert response.status_code == 422

    data = json.loads(response.data)

    assert data == {
        'errors': {
            'username': ['This field is required.']
        }
    }


def test_missing_email(api):
    user = get_user('admin')

    client = api.test_client()

    response = client.post('/forgot-password', data={
        'username': user.username,
    })

    assert response.status_code == 422

    data = json.loads(response.data)

    assert data == {
        'errors': {
            'email': ['This field is required.']
        }
    }


def test_user_not_found(api):
    client = api.test_client()

    response = client.post('/forgot-password', data={
        'username': '404',
        'email': '404@example.org',
    })

    assert response.status_code == 422

    data = json.loads(response.data)

    assert data == {
        'errors': {
            'username': ['No user found with that username and email.']
        }
    }

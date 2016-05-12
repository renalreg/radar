from datetime import datetime

from radar.auth.forgot_password import generate_reset_password_token
from radar.database import db
from tests.api.views.fixtures import get_user


STRONG_PASSWORD = 'qzm5zuLVgL1t'
WEAK_PASSWORD = 'password123'


def reset_password(user):
    token, token_hash = generate_reset_password_token()
    user.reset_password_token = token_hash
    user.reset_password_date = datetime.now()
    db.session.commit()
    return token


def test_reset_password(api):
    user = get_user('admin')
    token = reset_password(user)

    client1 = api.test_client()

    client2 = api.test_client()
    client2.login(user)

    assert client1.get('/patients').status_code == 401
    assert client2.get('/patients').status_code == 200

    response = client1.post('/reset-password', data={
        'token': token,
        'username': user.username,
        'password': STRONG_PASSWORD,
    })

    assert response.status_code == 200

    db.session.refresh(user)

    assert user.reset_password_token is None
    assert user.reset_password_date is None

    # Other user logged out
    assert client2.get('/patients').status_code == 401

    # Can login with new password
    client1.login(user, password=STRONG_PASSWORD)


def test_missing_username(api):
    user = get_user('admin')
    token = reset_password(user)

    client = api.test_client()

    response = client.post('/reset-password', data={
        'token': token,
        'password': STRONG_PASSWORD,
    })

    assert response.status_code == 422


def test_wrong_username(api):
    user = get_user('admin')
    token = reset_password(user)

    client = api.test_client()

    response = client.post('/reset-password', data={
        'token': token,
        'username': 'foo',
        'password': STRONG_PASSWORD,
    })

    assert response.status_code == 422


def test_missing_password(api):
    user = get_user('admin')
    token = reset_password(user)

    client = api.test_client()

    response = client.post('/reset-password', data={
        'token': token,
        'username': user.username,
    })

    assert response.status_code == 422


def test_weak_password(api):
    user = get_user('admin')
    token = reset_password(user)

    client = api.test_client()

    response = client.post('/reset-password', data={
        'token': token,
        'username': user.username,
        'password': WEAK_PASSWORD,
    })

    assert response.status_code == 422


def test_missing_token(api):
    user = get_user('admin')
    reset_password(user)

    client = api.test_client()

    response = client.post('/reset-password', data={
        'username': user.username,
        'password': STRONG_PASSWORD,
    })

    assert response.status_code == 422


def test_wrong_token(api):
    user = get_user('admin')
    reset_password(user)

    client = api.test_client()

    response = client.post('/reset-password', data={
        'token': '12345',
        'username': user.username,
        'password': STRONG_PASSWORD,
    })

    assert response.status_code == 422


def test_expired_token(api):
    user = get_user('admin')
    token = reset_password(user)

    user.reset_password_date = datetime(1990, 1, 1)
    db.session.commit()

    client = api.test_client()

    response = client.post('/reset-password', data={
        'token': token,
        'username': user.username,
        'password': STRONG_PASSWORD,
    })

    assert response.status_code == 422

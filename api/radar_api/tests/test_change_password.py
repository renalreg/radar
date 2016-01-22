import json

from radar_api.tests.fixtures import get_user
from radar.models.user_sessions import UserSession


def get_session_count(user):
    return UserSession.query.filter(UserSession.user == user, UserSession.is_active == True).count()  # noqa


def test_change_password(app):
    user = get_user('admin')
    old_password = 'password'
    new_password = 'qzm5zuLVgL1t'

    client1 = app.test_client()
    client1.login(user)

    client2 = app.test_client()
    client2.login(user)

    # Check both clients are logged in
    assert client1.get('/patients').status_code == 200
    assert client2.get('/patients').status_code == 200

    assert get_session_count(user) == 2

    assert client1.post('/users/%s' % user.id, data={
        'current_password': old_password,
        'password': new_password
    }).status_code == 200

    assert get_session_count(user) == 1

    # Check second client is logged out
    assert client1.get('/patients').status_code == 200
    assert client2.get('/patients').status_code == 401

    client2.login(user, password=new_password)

    assert get_session_count(user) == 2

    assert client2.get('/patients').status_code == 200


def test_incorrect_password(app):
    user = get_user('admin')

    client1 = app.test_client()
    client1.login(user)

    client2 = app.test_client()
    client2.login(user)

    # Check both clients are logged in
    assert client1.get('/patients').status_code == 200
    assert client2.get('/patients').status_code == 200

    assert get_session_count(user) == 2

    response = client1.post('/users/%s' % user.id, data={
        'current_password': 'foobarbaz',
        'password': 'qzm5zuLVgL1t'
    })

    assert response.status_code == 422

    data = json.loads(response.data)

    assert data == {
        'errors': {
            'current_password': ['Incorrect password!']
        }
    }

    assert get_session_count(user) == 2

    # Check both clients are still logged in
    assert client1.get('/patients').status_code == 200
    assert client2.get('/patients').status_code == 200


def test_weak_password(app):
    user = get_user('admin')

    client1 = app.test_client()
    client1.login(user)

    client2 = app.test_client()
    client2.login(user)

    response = client1.post('/users/%s' % user.id, data={
        'current_password': 'password',
        'password': 'password123'
    })

    assert response.status_code == 422

    data = json.loads(response.data)

    assert data == {
        'errors': {
            'password': ['Password is too weak.']
        }
    }

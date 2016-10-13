import json

from radar.models.user_sessions import UserSession
from tests.api.fixtures import get_user


def get_session_count(user):
    return UserSession.query.filter(UserSession.user == user).count()


def test_change_password(api):
    user = get_user('admin')
    old_password = 'password'
    new_password = 'qzm5zuLVgL1t'

    client1 = api.test_client()
    client1.login(user)

    client2 = api.test_client()
    client2.login(user)

    # Check both clients are logged in
    assert client1.get('/patients').status_code == 200
    assert client2.get('/patients').status_code == 200

    assert get_session_count(user) == 2

    assert client1.patch('/users/%s' % user.id, data={
        'currentPassword': old_password,
        'password': new_password
    }).status_code == 200

    assert get_session_count(user) == 1

    # Check second client is logged out
    assert client1.get('/patients').status_code == 200
    assert client2.get('/patients').status_code == 401

    client2.login(user, password=new_password)

    assert get_session_count(user) == 2

    assert client2.get('/patients').status_code == 200


def test_incorrect_password(api):
    user = get_user('admin')

    client1 = api.test_client()
    client1.login(user)

    client2 = api.test_client()
    client2.login(user)

    # Check both clients are logged in
    assert client1.get('/patients').status_code == 200
    assert client2.get('/patients').status_code == 200

    assert get_session_count(user) == 2

    response = client1.patch('/users/%s' % user.id, data={
        'currentPassword': 'foobarbaz',
        'password': 'qzm5zuLVgL1t'
    })

    assert response.status_code == 422

    data = json.loads(response.data)

    assert data == {
        'errors': {
            'currentPassword': ['Incorrect password!']
        }
    }

    assert get_session_count(user) == 2

    # Check both clients are still logged in
    assert client1.get('/patients').status_code == 200
    assert client2.get('/patients').status_code == 200


def test_weak_password(api):
    user = get_user('admin')

    client1 = api.test_client()
    client1.login(user)

    client2 = api.test_client()
    client2.login(user)

    response = client1.patch('/users/%s' % user.id, data={
        'currentPassword': 'password',
        'password': 'password123'
    })

    assert response.status_code == 422

    data = json.loads(response.data)

    assert data == {
        'errors': {
            'password': ['Password is too weak, try including an uppercase letter.']
        }
    }

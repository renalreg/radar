import json

from tests.api.views.fixtures import get_user


def login(client, username, password):
    response = client.post(
        '/login',
        data={
            'username': username,
            'password': password
        }
    )

    return response


def test_good_login(api):
    user = get_user('admin')

    client = api.test_client()

    response = login(client, 'admin', 'password')

    assert response.status_code == 200

    data = json.loads(response.data)

    assert data['userId'] == user.id
    assert 'token' in data


def test_bad_login(api):
    client = api.test_client()

    response = login(client, 'admin', 'foo')

    assert response.status_code == 422

    data = json.loads(response.data)

    assert data == {
        'errors': {
            'username': ['Incorrect username or password.']
        }
    }

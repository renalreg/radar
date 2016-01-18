import json

from radar_api.tests.fixtures import get_user


def test_serialization(app):
    admin = get_user('admin')

    client = app.test_client()
    client.login(admin)

    response = client.get('/users')

    assert response.status_code == 200

    data = json.loads(response.data)

    for user in data['data']:
        assert 'username' in user
        assert 'password_hash' not in user
        assert 'reset_password_token' not in user

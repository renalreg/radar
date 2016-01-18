import json

import pytest

from radar_api.tests.fixtures import get_user


@pytest.mark.parametrize(['username', 'other_username', 'expected'], [
    ('admin', 'null', 200),
    ('hospital1_admin', 'null', 403),
    ('hospital1_admin', 'hospital1_clinician', 422),
    ('hospital1_admin', 'hospital1_admin', 422),
])
def test_is_admin_true(app, username, other_username, expected):
    user = get_user(username)
    other_user = get_user(other_username)

    client = app.test_client()
    client.login(user)

    response = client.post('/users/%s' % other_user.id, data={
        'is_admin': True
    })

    assert response.status_code == expected


@pytest.mark.parametrize(['username', 'other_username', 'expected'], [
    ('admin', 'admin', 422),
    ('hospital1_admin', 'admin', 403),
    ('hospital1_admin', 'hospital1_admin', 200),
])
def test_is_admin_false(app, username, other_username, expected):
    user = get_user(username)
    other_user = get_user(other_username)

    client = app.test_client()
    client.login(user)

    response = client.post('/users/%s' % other_user.id, data={
        'is_admin': False
    })

    assert response.status_code == expected


@pytest.mark.parametrize(['username', 'other_username', 'expected'], [
    ('admin', 'admin', 422),
    ('admin', 'hospital1_clinician', 200),
    ('hospital1_admin', 'admin', 403),
    ('hospital1_admin', 'hospital1_admin', 422),
    ('hospital1_admin', 'hospital1_clinician', 200),
    ('hospital1_admin', 'hospital2_clinician', 403),
    ('hospital1_clinician', 'hospital1_clinician', 422),
    ('hospital1_clinician', 'hospital1_admin', 403),
])
def test_change_password(app, username, other_username, expected):
    user = get_user(username)
    other_user = get_user(other_username)

    client = app.test_client()
    client.login(user)

    response = client.post('/users/%s' % other_user.id, data={
        'password': 'qzm5zuLVgL1t'
    })

    assert response.status_code == expected


@pytest.mark.parametrize(['username', 'other_username', 'expected'], [
    ('admin', 'admin', 422),
    ('admin', 'hospital1_clinician', 200),
    ('hospital1_admin', 'admin', 403),
    ('hospital1_admin', 'hospital1_admin', 422),
    ('hospital1_admin', 'hospital1_clinician', 200),
    ('hospital1_admin', 'hospital2_clinician', 403),
    ('hospital1_clinician', 'hospital1_clinician', 422),
    ('hospital1_clinician', 'hospital1_admin', 403),
])
def test_change_email(app, username, other_username, expected):
    user = get_user(username)
    other_user = get_user(other_username)

    client = app.test_client()
    client.login(user)

    response = client.post('/users/%s' % other_user.id, data={
        'email': 'bar@example.org'
    })

    assert response.status_code == expected


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

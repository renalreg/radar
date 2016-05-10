import json
import itertools

import pytest

from radar.database import db
from radar.models.groups import GROUP_TYPE
from radar.models.users import User
from radar.roles import ROLE
from radar.tests.api.views.fixtures import get_user, create_user, add_user_to_group, get_group


def get_read_list_args():
    usernames = ['admin', 'hospital1_senior_clinician', 'hospital1_admin', 'hospital1_clinician', 'null']
    groups = [(GROUP_TYPE.HOSPITAL, 'HOSPITAL1', ROLE.CLINICIAN), (None, None, None)]

    for username, group, is_admin in itertools.product(usernames, groups, [False, True]):
        group_type, group_code, role = group

        if username == 'admin':
            expected = True
        elif username in ('hospital1_admin', 'hospital1_senior_clinician'):
            expected = True
        else:
            expected = False

        yield username, group_type, group_code, role, is_admin, expected


def get_read_args():
    return get_read_list_args()


def get_update_args():
    usernames = ['admin', 'hospital1_senior_clinician', 'hospital1_admin', 'null']
    groups = [(GROUP_TYPE.HOSPITAL, 'HOSPITAL1', ROLE.CLINICIAN), (None, None, None)]

    for username, group, is_admin in itertools.product(usernames, groups, [False, True]):
        group_type, group_code, role = group

        if username == 'admin':
            expected = True
        elif is_admin:
            expected = False
        elif username == 'hospital1_admin':
            expected = group_code == 'HOSPITAL1'
        else:
            expected = False

        yield username, group_type, group_code, role, is_admin, expected


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'role', 'is_admin', 'expected'], get_read_list_args())
def test_read_user_list(api, username, group_type, group_code, role, is_admin, expected):
    user = get_user(username)

    other_user = create_user('test', is_admin=is_admin)

    if group_type is not None:
        group = get_group(group_type, group_code)
        add_user_to_group(other_user, group, role)

    client = api.test_client()
    client.login(user)

    response = client.get('/users?id=%s' % other_user.id)

    assert response.status_code == 200

    data = json.loads(response.data)

    if expected:
        assert len(data['data']) == 1
    else:
        assert len(data['data']) == 0


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'role', 'is_admin', 'expected'], get_read_args())
def test_read_user(api, username, group_type, group_code, role, is_admin, expected):
    user = get_user(username)

    other_user = create_user('test', is_admin=is_admin)

    if group_type is not None:
        group = get_group(group_type, group_code)
        add_user_to_group(other_user, group, role)

    client = api.test_client()
    client.login(user)

    response = client.get('/users/%s' % other_user.id)

    if expected:
        assert response.status_code == 200
    else:
        assert response.status_code == 403


@pytest.mark.parametrize('username', ['admin', 'hospital1_senior_clinician', 'hospital1_admin', 'null'])
def test_read_self(api, username):
    user = get_user(username)

    client = api.test_client()
    client.login(user)

    response = client.get('/users/%s' % user.id)
    assert response.status_code == 200

    response = client.get('/users?id=%s' % user.id)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) == 1


@pytest.mark.parametrize(['username', 'expected'], [
    ('admin', True),
    ('hospital1_clinician', False),
    ('hospital1_senior_clinician', True),
    ('hospital1_admin', True),
    ('null', False),
])
def test_create_user(api, username, expected):
    user = get_user(username)

    client = api.test_client()
    client.login(user)

    response = client.post('/users', data={
        'username': 'test',
        'first_name': 'Bruce',
        'last_name': 'Wayne',
        'force_password_change': True,
        'password': 'qzm5zuLVgL1t',
        'email': 'foo@example.org',
    })

    created = User.query.filter(User.username == 'test').count() > 0

    if expected:
        assert response.status_code == 200
        assert created
    else:
        assert response.status_code == 403
        assert not created


@pytest.mark.parametrize(['username', 'group_type', 'group_code', 'role', 'is_admin', 'expected'], get_update_args())
def test_update_user(api, username, group_type, group_code, role, is_admin, expected):
    user = get_user(username)

    other_user = create_user('test', first_name='Foo', last_name='Bar', is_admin=is_admin)

    if group_type is not None:
        group = get_group(group_type, group_code)
        add_user_to_group(other_user, group, role)

    db.session.commit()

    client = api.test_client()
    client.login(user)

    response = client.patch('/users/%s' % other_user.id, data={
        'first_name': 'Bruce',
        'last_name': 'Wayne',
    })

    db.session.refresh(other_user)

    if expected:
        assert response.status_code == 200

        assert other_user.first_name == 'Bruce'
        assert other_user.last_name == 'Wayne'
    else:
        assert response.status_code == 403

        assert other_user.first_name == 'Foo'
        assert other_user.last_name == 'Bar'


@pytest.mark.parametrize('username', ['admin', 'hospital1_senior_clinician', 'hospital1_admin', 'null'])
def test_update_self(api, username):
    user = get_user(username)

    client = api.test_client()
    client.login(user)

    response = client.patch('/users/%s' % user.id, data={
        'first_name': 'Bruce',
        'last_name': 'Wayne',
    })

    db.session.refresh(user)

    assert response.status_code == 200

    assert user.first_name == 'Bruce'
    assert user.last_name == 'Wayne'


@pytest.mark.parametrize('username', ['admin', 'hospital1_senior_clinician', 'hospital1_admin', 'null'])
def test_delete_self(api, username):
    user = get_user(username)

    client = api.test_client()
    client.login(user)

    response = client.delete('/users/%s' % user.id)

    # Not possible to delete yourself
    assert response.status_code == 403

    user = User.query.get(user.id)

    assert user is not None


@pytest.mark.parametrize(['username', 'other_username', 'expected'], [
    ('admin', 'null', 200),
    ('hospital1_admin', 'null', 403),
    ('hospital1_admin', 'hospital1_clinician', 422),
    ('hospital1_admin', 'hospital1_admin', 422),
])
def test_is_admin_true(api, username, other_username, expected):
    user = get_user(username)
    other_user = get_user(other_username)

    client = api.test_client()
    client.login(user)

    response = client.patch('/users/%s' % other_user.id, data={
        'is_admin': True
    })

    assert response.status_code == expected


@pytest.mark.parametrize(['username', 'other_username', 'expected'], [
    ('admin', 'admin', 422),
    ('hospital1_admin', 'admin', 403),
    ('hospital1_admin', 'hospital1_admin', 200),
])
def test_is_admin_false(api, username, other_username, expected):
    user = get_user(username)
    other_user = get_user(other_username)

    client = api.test_client()
    client.login(user)

    response = client.patch('/users/%s' % other_user.id, data={
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
def test_change_password(api, username, other_username, expected):
    user = get_user(username)
    other_user = get_user(other_username)

    client = api.test_client()
    client.login(user)

    response = client.patch('/users/%s' % other_user.id, data={
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
def test_change_email(api, username, other_username, expected):
    user = get_user(username)
    other_user = get_user(other_username)

    client = api.test_client()
    client.login(user)

    response = client.patch('/users/%s' % other_user.id, data={
        'email': 'bar@example.org'
    })

    assert response.status_code == expected


def test_serialization(api):
    admin = get_user('admin')

    client = api.test_client()
    client.login(admin)

    response = client.get('/users')

    assert response.status_code == 200

    data = json.loads(response.data)

    for user in data['data']:
        assert 'username' in user
        assert 'password' not in user
        assert 'password_hash' not in user
        assert 'reset_password_token' not in user

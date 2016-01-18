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

    print get_session_count(user)

    assert client1.post('/users/%s' % user.id, data={
        'current_password': old_password,
        'password': new_password
    }).status_code == 200

    print get_session_count(user)

    # Check second client is logged out
    assert client1.get('/patients').status_code == 200
    assert client2.get('/patients').status_code == 401

    client2.login(user, password=new_password)

    assert client2.get('/patients').status_code == 200

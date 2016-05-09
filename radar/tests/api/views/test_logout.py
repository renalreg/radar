from radar.models.user_sessions import UserSession
from radar.tests.api.views.fixtures import get_user


def get_session_count(user):
    return UserSession.query.filter(UserSession.user == user).count()


def test_logout(app):
    user = get_user('admin')

    client = app.test_client()

    assert get_session_count(user) == 0

    client.login(user)

    assert get_session_count(user) == 1

    response = client.get('/patients')
    assert response.status_code == 200

    response = client.post('/logout')
    assert response.status_code == 200

    assert get_session_count(user) == 0

    response = client.get('/patients')
    assert response.status_code == 401

    response = client.post('/logout')
    assert response.status_code == 401

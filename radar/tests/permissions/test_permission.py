from radar.permissions import Permission
from radar.tests.permissions.helpers import MockRequest, make_user


def test_has_permission():
    permission = Permission()
    request = MockRequest('GET')
    user = make_user()

    assert permission.has_permission(request, user)


def test_has_object_permission():
    permission = Permission()
    request = MockRequest('GET')
    user = make_user()

    assert permission.has_object_permission(request, user, object())

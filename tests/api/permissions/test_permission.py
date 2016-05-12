from radar.api.permissions import Permission
from tests.permissions.helpers import make_user
from tests.api.permissions.helpers import MockRequest


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

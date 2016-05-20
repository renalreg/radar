from radar.api.permissions import AdminPermission
from tests.api.permissions.helpers import MockRequest, MockPermission
from tests.permissions.helpers import make_user


def test_super():
    class MockAdminPermission(AdminPermission, MockPermission):
        pass

    request = MockRequest('GET')
    user = make_user()

    permission = MockAdminPermission()
    assert not permission.has_permission(request, user)
    assert permission.has_permission_called

    user.is_admin = True

    permission = MockAdminPermission()
    assert permission.has_permission(request, user)
    assert permission.has_permission_called


def test_has_permission():
    permission = AdminPermission()
    request = MockRequest('GET')
    user = make_user()

    assert not permission.has_permission(request, user)

    user.is_admin = True

    assert permission.has_permission(request, user)


def test_has_object_permission():
    permission = AdminPermission()
    request = MockRequest('GET')
    user = make_user()

    assert not permission.has_object_permission(request, user, object())

    user.is_admin = True

    assert permission.has_object_permission(request, user, object())

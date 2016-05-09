from radar.api.permissions import Permission


class MockRequest(object):
    def __init__(self, method):
        self.method = method


class MockPermission(Permission):
    def __init__(self):
        self.has_permission_called = False
        self.has_object_permission_called = False

    def has_permission(self, request, user):
        self.has_permission_called = True
        return True

    def has_object_permission(self, request, user, obj):
        self.has_object_permission_called = True
        return True

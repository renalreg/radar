from radar.models.groups import Group, GroupPatient, GroupUser
from radar.models.patients import Patient
from radar.models.users import User
from radar.permissions import Permission


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


def make_groups(n):
    return [Group() for _ in range(n)]


def make_patient(groups=None):
    if groups is None:
        groups = []

    patient = Patient()

    for group in groups:
        group_patient = GroupPatient()
        group_patient.group = group
        group_patient.patient = patient

    return patient


def make_user(groups=None):
    if groups is None:
        groups = []

    user = User()

    for group in groups:
        if isinstance(group, GroupUser):
            group_user = group
        else:
            try:
                group, role = group
            except (TypeError, ValueError):
                role = None

            group_user = GroupUser()
            group_user.group = group
            group_user.user = user
            group_user.role = role

        user.group_users.append(group_user)

    return user

from radar.roles import ROLES, PERMISSIONS
from radar.models.groups import GroupUser


def test_permissions():
    obj = GroupUser()
    obj.role = ROLES.RESEARCHER
    assert obj.permissions == [
        PERMISSIONS.VIEW_PATIENT,
    ]


def test_role():
    obj = GroupUser()
    obj.role = ROLES.RESEARCHER
    assert obj.role is ROLES.RESEARCHER
    assert obj._role is ROLES.RESEARCHER.value

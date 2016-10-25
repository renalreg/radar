from radar.models.groups import GroupUser
from radar.roles import ROLE, PERMISSION


def test_permissions():
    obj = GroupUser()
    obj.role = ROLE.RESEARCHER
    assert obj.permissions == [
        PERMISSION.VIEW_PATIENT,
    ]


def test_role():
    obj = GroupUser()
    obj.role = ROLE.RESEARCHER
    assert obj.role is ROLE.RESEARCHER

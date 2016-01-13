from radar.roles import ROLE, PERMISSION
from radar.models.groups import GroupUser


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
    assert obj._role is ROLE.RESEARCHER.value

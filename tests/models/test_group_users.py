from radar.models.groups import GroupUser
from radar.roles import PERMISSION, ROLE


def test_permissions():
    obj = GroupUser()
    obj.role = ROLE.RESEARCHER

    def sort_func(x):
        return x.value

    expected_roles = sorted([PERMISSION.VIEW_PATIENT, PERMISSION.VIEW_COHORT], key=sort_func)
    assert sorted(obj.permissions, key=sort_func) == expected_roles


def test_role():
    obj = GroupUser()
    obj.role = ROLE.RESEARCHER
    assert obj.role is ROLE.RESEARCHER

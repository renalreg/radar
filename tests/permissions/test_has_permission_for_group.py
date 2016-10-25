from radar.models.groups import Group
from radar.permissions import has_permission_for_group
from radar.roles import ROLE, PERMISSION
from tests.permissions.helpers import make_user, make_groups


def test_admin():
    user = make_user()
    group = Group()

    assert not has_permission_for_group(user, group, PERMISSION.VIEW_PATIENT)

    user.is_admin = True

    assert has_permission_for_group(user, group, PERMISSION.VIEW_PATIENT)


def test_not_in_group():
    group_a, group_b = make_groups(2)
    user = make_user([(group_a, ROLE.RESEARCHER)])

    assert has_permission_for_group(user, group_a, PERMISSION.VIEW_PATIENT)
    assert not has_permission_for_group(user, group_b, PERMISSION.VIEW_PATIENT)


def test_in_group_with_permission():
    group = Group()
    user = make_user([(group, ROLE.RESEARCHER)])

    assert has_permission_for_group(user, group, PERMISSION.VIEW_PATIENT)


def test_in_group_without_permission():
    group = Group()
    group_researcher_user = make_user([(group, ROLE.RESEARCHER)])
    group_senior_researcher_user = make_user([(group, ROLE.SENIOR_RESEARCHER)])

    assert not has_permission_for_group(group_researcher_user, group, PERMISSION.VIEW_DEMOGRAPHICS)
    assert has_permission_for_group(group_senior_researcher_user, group, PERMISSION.VIEW_DEMOGRAPHICS)

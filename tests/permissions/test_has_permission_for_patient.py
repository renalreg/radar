from radar.models.groups import Group
from radar.permissions import has_permission_for_patient
from radar.roles import PERMISSION, ROLE
from tests.permissions.helpers import make_groups, make_patient, make_user


def should_grant(user, patient, permission):
    assert has_permission_for_patient(user, patient, permission)


def should_deny(user, patient, permission):
    assert not has_permission_for_patient(user, patient, permission)


def test_admin():
    user = make_user()
    patient = make_patient()

    should_deny(user, patient, PERMISSION.VIEW_DEMOGRAPHICS)

    user.is_admin = True

    should_grant(user, patient, PERMISSION.VIEW_DEMOGRAPHICS)


def test_intersecting_groups():
    group = Group()
    patient = make_patient([group])
    user_a = make_user([(group, ROLE.RESEARCHER)])
    user_b = make_user([(group, ROLE.SENIOR_RESEARCHER)])

    should_deny(user_a, patient, PERMISSION.VIEW_DEMOGRAPHICS)
    should_grant(user_b, patient, PERMISSION.VIEW_DEMOGRAPHICS)


def test_disjoint_groups():
    group_a, group_b = make_groups(2)
    patient = make_patient([group_a])
    user_a = make_user([(group_b, ROLE.RESEARCHER)])
    user_b = make_user([(group_b, ROLE.SENIOR_RESEARCHER)])

    should_deny(user_a, patient, PERMISSION.VIEW_DEMOGRAPHICS)
    should_deny(user_b, patient, PERMISSION.VIEW_DEMOGRAPHICS)

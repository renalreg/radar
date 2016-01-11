from radar.permissions import has_permission_for_patient
from radar.tests.permissions.helpers import make_user, make_patient, make_groups
from radar.models.groups import Group
from radar.roles import ROLES, PERMISSIONS


def should_grant(user, patient, permission):
    assert has_permission_for_patient(user, patient, permission)


def should_deny(user, patient, permission):
    assert not has_permission_for_patient(user, patient, permission)


def test_admin():
    user = make_user()
    patient = make_patient()

    should_deny(user, patient, PERMISSIONS.VIEW_DEMOGRAPHICS)

    user.is_admin = True

    should_grant(user, patient, PERMISSIONS.VIEW_DEMOGRAPHICS)


def test_intersecting_groups():
    group = Group()
    patient = make_patient([group])
    user_a = make_user([(group, ROLES.RESEARCHER)])
    user_b = make_user([(group, ROLES.SENIOR_RESEARCHER)])

    should_deny(user_a, patient, PERMISSIONS.VIEW_DEMOGRAPHICS)
    should_grant(user_b, patient, PERMISSIONS.VIEW_DEMOGRAPHICS)


def test_disjoint_groups():
    group_a, group_b = make_groups(2)
    patient = make_patient([group_a])
    user_a = make_user([(group_b, ROLES.RESEARCHER)])
    user_b = make_user([(group_b, ROLES.SENIOR_RESEARCHER)])

    should_deny(user_a, patient, PERMISSIONS.VIEW_DEMOGRAPHICS)
    should_deny(user_b, patient, PERMISSIONS.VIEW_DEMOGRAPHICS)

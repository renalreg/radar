from radar.models.groups import Group
from radar.permissions import can_edit_patient_object
from radar.roles import ROLES
from radar.tests.permissions.helpers import make_patient, make_user, make_groups


def test_admin():
    group = Group()
    patient = make_patient()
    user = make_user()

    assert not can_edit_patient_object(user, patient, group)

    user.is_admin = True

    assert can_edit_patient_object(user, patient, group)


def test_groups():
    group_a, group_b = make_groups(2)
    patient = make_patient([group_a])
    user = make_user([[group_a, ROLES.CLINICIAN]])

    assert can_edit_patient_object(user, patient, group_a)
    assert not can_edit_patient_object(user, patient, group_b)

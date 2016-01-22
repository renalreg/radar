from radar.models.groups import Group
from radar.permissions import PatientPermission, PatientObjectPermission
from radar.roles import ROLE
from radar.tests.permissions.helpers import MockRequest, make_user, make_patient, make_groups


class MockObj(object):
    def __init__(self, patient):
        self.patient = patient


def make_read_request():
    return MockRequest('GET')


def make_write_request():
    return MockRequest('POST')


def should_grant(request, user, patient):
    patient_permission = PatientPermission()
    assert patient_permission.has_object_permission(request, user, patient)

    patient_object_permission = PatientObjectPermission()
    obj = MockObj(patient)
    assert patient_object_permission.has_object_permission(request, user, obj)


def should_deny(request, user, patient):
    patient_permission = PatientPermission()
    assert not patient_permission.has_object_permission(request, user, patient)

    patient_object_permission = PatientObjectPermission()
    obj = MockObj(patient)
    assert not patient_object_permission.has_object_permission(request, user, obj)


def test_admin():
    user = make_user()
    patient = make_patient()
    read_request = make_read_request()
    write_request = make_write_request()

    should_deny(read_request, user, patient)
    should_deny(write_request, user, patient)

    user.is_admin = True

    should_grant(read_request, user, patient)
    should_grant(write_request, user, patient)


def test_intersecting_groups():
    group = Group()
    patient = make_patient([group])
    user = make_user([(group, ROLE.RESEARCHER)])
    read_request = make_read_request()
    write_request = make_write_request()

    should_grant(read_request, user, patient)
    should_deny(write_request, user, patient)


def test_disjoint_groups():
    group_a, group_b = make_groups(2)
    patient = make_patient([group_a])
    user_a = make_user([(group_a, ROLE.RESEARCHER)])
    user_b = make_user([(group_b, ROLE.RESEARCHER)])
    read_request = make_read_request()
    write_request = make_write_request()

    should_grant(read_request, user_a, patient)
    should_deny(read_request, user_b, patient)

    should_deny(write_request, user_a, patient)
    should_deny(write_request, user_b, patient)

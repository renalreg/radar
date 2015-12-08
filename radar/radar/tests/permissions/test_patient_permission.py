from radar.models import Organisation
from radar.permissions import PatientPermission, PatientObjectPermission
from radar.roles import COHORT_ROLES, ORGANISATION_ROLES
from radar.tests.permissions.helpers import MockRequest, make_user, make_patient, make_cohorts, make_organisations
from radar.models.cohorts import Cohort


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


def test_intersecting_cohorts():
    cohort = Cohort()
    patient = make_patient(cohorts=[cohort])
    user = make_user(cohorts=[(cohort, COHORT_ROLES.RESEARCHER)])
    read_request = make_read_request()
    write_request = make_write_request()

    should_grant(read_request, user, patient)
    should_deny(write_request, user, patient)


def test_intersecting_organisations():
    organisation = Organisation()
    patient = make_patient(organisations=[organisation])
    user = make_user(organisations=[(organisation, ORGANISATION_ROLES.CLINICIAN)])
    read_request = make_read_request()
    write_request = make_write_request()

    should_grant(read_request, user, patient)
    should_grant(write_request, user, patient)


def test_disjoint_cohorts():
    cohort_a, cohort_b = make_cohorts(2)
    patient = make_patient(cohorts=[cohort_a])
    user_a = make_user(cohorts=[(cohort_a, COHORT_ROLES.RESEARCHER)])
    user_b = make_user(cohorts=[(cohort_b, COHORT_ROLES.RESEARCHER)])
    read_request = make_read_request()
    write_request = make_write_request()

    should_grant(read_request, user_a, patient)
    should_deny(read_request, user_b, patient)

    should_deny(write_request, user_a, patient)
    should_deny(write_request, user_b, patient)


def test_disjoint_organisations():
    organisation_a, organisation_b = make_organisations(2)
    patient = make_patient(organisations=[organisation_a])
    user_a = make_user(organisations=[(organisation_a, ORGANISATION_ROLES.CLINICIAN)])
    user_b = make_user(organisations=[(organisation_b, ORGANISATION_ROLES.CLINICIAN)])
    read_request = make_read_request()
    write_request = make_write_request()

    should_grant(read_request, user_a, patient)
    should_deny(read_request, user_b, patient)

    should_grant(write_request, user_a, patient)
    should_deny(write_request, user_b, patient)

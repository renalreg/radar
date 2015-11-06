from radar.models import Organisation
from radar.permissions import PatientPermission
from radar.roles import COHORT_RESEARCHER, ORGANISATION_CLINICIAN
from radar.tests.permissions.helpers import MockRequest, make_user, make_patient, make_cohorts, make_organisations
from radar.models.cohorts import Cohort


def make_read_request():
    return MockRequest('GET')


def make_write_request():
    return MockRequest('POST')


def should_grant(request, user, obj):
    permission = PatientPermission()
    assert permission.has_object_permission(request, user, obj)


def should_deny(request, user, obj):
    permission = PatientPermission()
    assert not permission.has_object_permission(request, user, obj)


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
    user = make_user(cohorts=[(cohort, COHORT_RESEARCHER)])
    read_request = make_read_request()
    write_request = make_write_request()

    should_grant(read_request, user, patient)
    should_deny(write_request, user, patient)


def test_intersecting_organisations():
    organisation = Organisation()
    patient = make_patient(organisations=[organisation])
    user = make_user(organisations=[(organisation, ORGANISATION_CLINICIAN)])
    read_request = make_read_request()
    write_request = make_write_request()

    should_grant(read_request, user, patient)
    should_grant(write_request, user, patient)


def test_disjoint_cohorts():
    cohort_a, cohort_b = make_cohorts(2)
    patient = make_patient(cohorts=[cohort_a])
    user_a = make_user(cohorts=[(cohort_a, COHORT_RESEARCHER)])
    user_b = make_user(cohorts=[(cohort_b, COHORT_RESEARCHER)])
    read_request = make_read_request()
    write_request = make_write_request()

    should_grant(read_request, user_a, patient)
    should_deny(read_request, user_b, patient)

    should_deny(write_request, user_a, patient)
    should_deny(write_request, user_b, patient)


def test_disjoint_organisations():
    organisation_a, organisation_b = make_organisations(2)
    patient = make_patient(organisations=[organisation_a])
    user_a = make_user(organisations=[(organisation_a, ORGANISATION_CLINICIAN)])
    user_b = make_user(organisations=[(organisation_b, ORGANISATION_CLINICIAN)])
    read_request = make_read_request()
    write_request = make_write_request()

    should_grant(read_request, user_a, patient)
    should_deny(read_request, user_b, patient)

    should_grant(write_request, user_a, patient)
    should_deny(write_request, user_b, patient)

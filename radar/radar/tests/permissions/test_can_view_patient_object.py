from radar.models.cohorts import Cohort
from radar.models.organisations import Organisation
from radar.permissions import can_view_patient_object
from radar.roles import ORGANISATION_CLINICIAN, COHORT_RESEARCHER
from radar.tests.permissions.helpers import make_patient, make_user, \
    make_cohorts, make_organisations


def test_admin():
    cohort = Cohort()
    patient = make_patient()
    user = make_user()

    assert not can_view_patient_object(user, patient, cohort)

    user.is_admin = True

    assert can_view_patient_object(user, patient, cohort)


def test_cohort_user_no_permissions():
    cohort_a, cohort_b = make_cohorts(2)
    patient = make_patient(cohorts=[cohort_a])
    user = make_user(cohorts=[cohort_b, COHORT_RESEARCHER])

    assert not can_view_patient_object(user, patient, cohort_a)


def test_cohort_user_patient_and_cohort_permissions():
    cohort = Cohort()
    patient = make_patient(cohorts=[cohort])
    user = make_user(cohorts=[[cohort, COHORT_RESEARCHER]])

    assert can_view_patient_object(user, patient, cohort)


def test_cohort_user_patient_and_no_cohort_permissions():
    cohort_a, cohort_b = make_cohorts(2)
    patient = make_patient(cohorts=[cohort_a])
    user = make_user(cohorts=[[cohort_a, COHORT_RESEARCHER]])

    assert can_view_patient_object(user, patient, cohort_a)
    assert not can_view_patient_object(user, patient, cohort_b)


def test_cohort_user_no_patient_and_cohort_permissions():
    cohort_a, cohort_b = make_cohorts(2)
    patient_a = make_patient(cohorts=[cohort_a])
    patient_b = make_patient(cohorts=[cohort_b])
    user = make_user(cohorts=[[cohort_b, COHORT_RESEARCHER]])

    assert not can_view_patient_object(user, patient_a, cohort_b)
    assert can_view_patient_object(user, patient_b, cohort_b)


def test_organisation_user_no_permissions():
    cohort = Cohort()
    organisation_a, organisation_b = make_organisations(2)
    patient = make_patient(organisations=[organisation_a])
    user = make_user(organisations=[organisation_b, ORGANISATION_CLINICIAN])

    assert not can_view_patient_object(user, patient, cohort)


def test_organisation_user_patient_and_cohort_permissions():
    cohort = Cohort()
    organisation = Organisation()
    patient = make_patient(organisations=[organisation])
    user = make_user(organisations=[[organisation, ORGANISATION_CLINICIAN]])

    assert can_view_patient_object(user, patient, cohort)

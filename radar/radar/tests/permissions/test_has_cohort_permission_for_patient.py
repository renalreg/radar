from radar.permissions import has_cohort_permission_for_patient, \
    has_group_permission_for_patient
from radar.tests.permissions.helpers import make_user, make_patient, make_cohorts
from radar.models.cohorts import Cohort
from radar.roles import COHORT_RESEARCHER, COHORT_SENIOR_RESEARCHER

VIEW_DEMOGRAPHICS = 'has_view_demographics_permission'


def should_grant(user, patient, permission):
    assert has_cohort_permission_for_patient(user, patient, permission)


def should_deny(user, patient, permission):
    assert not has_cohort_permission_for_patient(user, patient, permission)
    assert not has_group_permission_for_patient(user, patient, permission)


def test_admin():
    user = make_user()
    patient = make_patient()

    should_deny(user, patient, VIEW_DEMOGRAPHICS)

    user.is_admin = True

    should_grant(user, patient, VIEW_DEMOGRAPHICS)


def test_intersecting_cohorts():
    cohort = Cohort()
    patient = make_patient(cohorts=[cohort])
    user_a = make_user(cohorts=[(cohort, COHORT_RESEARCHER)])
    user_b = make_user(cohorts=[(cohort, COHORT_SENIOR_RESEARCHER)])

    should_deny(user_a, patient, VIEW_DEMOGRAPHICS)
    should_grant(user_b, patient, VIEW_DEMOGRAPHICS)


def test_disjoint_cohorts():
    cohort_a, cohort_b = make_cohorts(2)
    patient = make_patient(cohorts=[cohort_a])
    user_a = make_user(cohorts=[(cohort_b, COHORT_RESEARCHER)])
    user_b = make_user(cohorts=[(cohort_b, COHORT_SENIOR_RESEARCHER)])

    should_deny(user_a, patient, VIEW_DEMOGRAPHICS)
    should_deny(user_b, patient, VIEW_DEMOGRAPHICS)

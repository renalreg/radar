from radar.permissions import has_permission_for_cohort
from radar.models.cohorts import Cohort
from radar.roles import COHORT_RESEARCHER, COHORT_SENIOR_RESEARCHER
from radar.tests.permissions.helpers import make_user, make_cohorts


def test_admin():
    user = make_user()
    cohort = Cohort()

    assert not has_permission_for_cohort(user, cohort, 'has_view_patient_permission')

    user.is_admin = True

    assert has_permission_for_cohort(user, cohort, 'has_view_patient_permission')


def test_not_in_cohort():
    cohort_a, cohort_b = make_cohorts(2)
    user = make_user(cohorts=[(cohort_a, COHORT_RESEARCHER)])

    assert has_permission_for_cohort(user, cohort_a, 'has_view_patient_permission')
    assert not has_permission_for_cohort(user, cohort_b, 'has_view_patient_permission')


def test_in_cohort_with_permission():
    cohort = Cohort()
    user = make_user(cohorts=[(cohort, COHORT_RESEARCHER)])

    assert has_permission_for_cohort(user, cohort, 'has_view_patient_permission')


def test_in_cohort_without_permission():
    cohort = Cohort()
    cohort_researcher_user = make_user(cohorts=[(cohort, COHORT_RESEARCHER)])
    cohort_senior_researcher_user = make_user(cohorts=[(cohort, COHORT_SENIOR_RESEARCHER)])

    assert not has_permission_for_cohort(cohort_researcher_user, cohort, 'has_view_demographics_permission')
    assert has_permission_for_cohort(cohort_senior_researcher_user, cohort, 'has_view_demographics_permission')

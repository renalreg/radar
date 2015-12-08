from radar.permissions import has_permission_for_cohort
from radar.models.cohorts import Cohort
from radar.roles import COHORT_ROLES, PERMISSIONS
from radar.tests.permissions.helpers import make_user, make_cohorts


def test_admin():
    user = make_user()
    cohort = Cohort()

    assert not has_permission_for_cohort(user, cohort, PERMISSIONS.VIEW_PATIENT)

    user.is_admin = True

    assert has_permission_for_cohort(user, cohort, PERMISSIONS.VIEW_PATIENT)


def test_not_in_cohort():
    cohort_a, cohort_b = make_cohorts(2)
    user = make_user(cohorts=[(cohort_a, COHORT_ROLES.RESEARCHER)])

    assert has_permission_for_cohort(user, cohort_a, PERMISSIONS.VIEW_PATIENT)
    assert not has_permission_for_cohort(user, cohort_b, PERMISSIONS.VIEW_PATIENT)


def test_in_cohort_with_permission():
    cohort = Cohort()
    user = make_user(cohorts=[(cohort, COHORT_ROLES.RESEARCHER)])

    assert has_permission_for_cohort(user, cohort, PERMISSIONS.VIEW_PATIENT)


def test_in_cohort_without_permission():
    cohort = Cohort()
    cohort_researcher_user = make_user(cohorts=[(cohort, COHORT_ROLES.RESEARCHER)])
    cohort_senior_researcher_user = make_user(cohorts=[(cohort, COHORT_ROLES.SENIOR_RESEARCHER)])

    assert not has_permission_for_cohort(cohort_researcher_user, cohort, PERMISSIONS.VIEW_DEMOGRAPHICS)
    assert has_permission_for_cohort(cohort_senior_researcher_user, cohort, PERMISSIONS.VIEW_DEMOGRAPHICS)

from radar.roles import COHORT_ROLES, PERMISSIONS
from radar.models.cohorts import CohortUser


def test_permissions():
    obj = CohortUser()
    obj.role = COHORT_ROLES.RESEARCHER
    assert obj.permissions == [
        PERMISSIONS.VIEW_PATIENT,
    ]

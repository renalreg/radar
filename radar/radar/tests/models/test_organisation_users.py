from radar.roles import ORGANISATION_ROLES, PERMISSIONS
from radar.models.organisations import OrganisationUser


def test_permissions():
    obj = OrganisationUser()
    obj.role = ORGANISATION_ROLES.CLINICIAN
    assert obj.permissions == [
        PERMISSIONS.EDIT_PATIENT,
        PERMISSIONS.RECRUIT_PATIENT,
        PERMISSIONS.VIEW_DEMOGRAPHICS,
        PERMISSIONS.VIEW_PATIENT,
    ]

from radar.permissions import has_permission_for_organisation
from radar.models.organisations import Organisation
from radar.roles import ORGANISATION_ROLES, PERMISSIONS
from radar.tests.permissions.helpers import make_user, make_organisations


def test_admin():
    user = make_user()
    organisation = Organisation()

    assert not has_permission_for_organisation(user, organisation, PERMISSIONS.VIEW_PATIENT)

    user.is_admin = True

    assert has_permission_for_organisation(user, organisation, PERMISSIONS.VIEW_PATIENT)


def test_not_in_organisation():
    organisation_a, organisation_b = make_organisations(2)
    user = make_user(organisations=[(organisation_a, ORGANISATION_ROLES.CLINICIAN)])

    assert has_permission_for_organisation(user, organisation_a, PERMISSIONS.VIEW_PATIENT)
    assert not has_permission_for_organisation(user, organisation_b, PERMISSIONS.VIEW_PATIENT)


def test_in_organisation_with_permission():
    organisation = Organisation()
    user = make_user(organisations=[(organisation, ORGANISATION_ROLES.CLINICIAN)])

    assert has_permission_for_organisation(user, organisation, PERMISSIONS.VIEW_PATIENT)


def test_in_cohort_without_permission():
    organisation = Organisation()
    organisation_it_user = make_user(organisations=[(organisation, ORGANISATION_ROLES.IT)])
    organisation_clinician_user = make_user(organisations=[(organisation, ORGANISATION_ROLES.CLINICIAN)])

    assert not has_permission_for_organisation(organisation_it_user, organisation, PERMISSIONS.VIEW_DEMOGRAPHICS)
    assert has_permission_for_organisation(organisation_clinician_user, organisation, PERMISSIONS.VIEW_DEMOGRAPHICS)

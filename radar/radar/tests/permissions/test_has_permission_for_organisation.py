from radar.permissions import has_permission_for_organisation
from radar.models.organisations import Organisation
from radar.roles import ORGANISATION_IT, ORGANISATION_CLINICIAN
from radar.tests.permissions.helpers import make_user, make_organisations


def test_admin():
    user = make_user()
    organisation = Organisation()

    assert not has_permission_for_organisation(user, organisation, 'has_view_patient_permission')

    user.is_admin = True

    assert has_permission_for_organisation(user, organisation, 'has_view_patient_permission')


def test_not_in_organisation():
    organisation_a, organisation_b = make_organisations(2)
    user = make_user(organisations=[(organisation_a, ORGANISATION_CLINICIAN)])

    assert has_permission_for_organisation(user, organisation_a, 'has_view_patient_permission')
    assert not has_permission_for_organisation(user, organisation_b, 'has_view_patient_permission')


def test_in_organisation_with_permission():
    organisation = Organisation()
    user = make_user(organisations=[(organisation, ORGANISATION_CLINICIAN)])

    assert has_permission_for_organisation(user, organisation, 'has_view_patient_permission')


def test_in_cohort_without_permission():
    organisation = Organisation()
    organisation_it_user = make_user(organisations=[(organisation, ORGANISATION_IT)])
    organisation_clinician_user = make_user(organisations=[(organisation, ORGANISATION_CLINICIAN)])

    assert not has_permission_for_organisation(organisation_it_user, organisation, 'has_view_demographics_permission')
    assert has_permission_for_organisation(organisation_clinician_user, organisation, 'has_view_demographics_permission')

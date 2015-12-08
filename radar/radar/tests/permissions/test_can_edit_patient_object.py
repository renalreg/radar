from radar.models.organisations import Organisation
from radar.permissions import can_edit_patient_object
from radar.roles import ORGANISATION_ROLES
from radar.tests.permissions.helpers import make_patient, make_user, make_organisations


def test_admin():
    organisation = Organisation()
    patient = make_patient()
    user = make_user()

    assert not can_edit_patient_object(user, patient, organisation)

    user.is_admin = True

    assert can_edit_patient_object(user, patient, organisation)


def test_no_permissions():
    organisation_a, organisation_b = make_organisations(2)
    patient = make_patient(organisations=[organisation_a])
    user = make_user(organisations=[organisation_b, ORGANISATION_ROLES.CLINICIAN])

    assert not can_edit_patient_object(user, patient, organisation_a)


def test_patient_and_organisation_permissions():
    organisation = Organisation()
    patient = make_patient(organisations=[organisation])
    user = make_user(organisations=[[organisation, ORGANISATION_ROLES.CLINICIAN]])

    assert can_edit_patient_object(user, patient, organisation)


def test_patient_and_no_organisation_permissions():
    organisation_a, organisation_b = make_organisations(2)
    patient = make_patient(organisations=[organisation_a])
    user = make_user(organisations=[[organisation_a, ORGANISATION_ROLES.CLINICIAN]])

    assert can_edit_patient_object(user, patient, organisation_a)
    assert not can_edit_patient_object(user, patient, organisation_b)


def test_no_patient_and_organisation_permissions():
    organisation_a, organisation_b = make_organisations(2)
    patient_a = make_patient(organisations=[organisation_a])
    patient_b = make_patient(organisations=[organisation_b])
    user = make_user(organisations=[[organisation_b, ORGANISATION_ROLES.CLINICIAN]])

    assert not can_edit_patient_object(user, patient_a, organisation_b)
    assert can_edit_patient_object(user, patient_b, organisation_b)

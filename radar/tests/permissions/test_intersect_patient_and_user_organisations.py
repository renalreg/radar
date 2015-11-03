from radar.permissions import intersect_patient_and_user_organisations as intersect
from radar.models.patients import Patient
from radar.models.users import User
from radar.models.organisations import Organisation, OrganisationUser, OrganisationPatient


def test_empty():
    patient = make_patient()
    user = make_user()

    assert intersect(patient, user) == []
    assert intersect(patient, user, patient_membership=True) == []
    assert intersect(patient, user, user_membership=True) == []
    assert intersect(patient, user, patient_membership=True, user_membership=True) == []


def test_intersection():
    a, b, c, d = make_organisations(4)

    patient = make_patient([a, b, c])
    p_a, p_b, p_c = patient.organisation_patients

    user = make_user([b, c, d])
    u_b, u_c, u_d = user.organisation_users

    assert intersect(patient, user) == [b, c]
    assert intersect(patient, user, patient_membership=True) == [p_b, p_c]
    assert intersect(patient, user, user_membership=True) == [u_b, u_c]
    assert intersect(patient, user, patient_membership=True, user_membership=True) == [
        (p_b, u_b),
        (p_c, u_c),
    ]


def test_disjoint():
    a, b, c, d = make_organisations(4)

    patient = make_patient([a, b])
    p_a, p_b = patient.organisation_patients

    user = make_user([c, d])
    u_c, u_d = user.organisation_users

    assert intersect(patient, user) == []
    assert intersect(patient, user, patient_membership=True) == []
    assert intersect(patient, user, user_membership=True) == []
    assert intersect(patient, user, patient_membership=True, user_membership=True) == []


def test_admin():
    a, b, c = make_organisations(3)

    patient = make_patient([a, b])
    p_a, p_b = patient.organisation_patients

    user = make_user([b, c])
    user.is_admin = True
    u_b, u_c = user.organisation_users

    assert intersect(patient, user) == [b]
    assert intersect(patient, user, patient_membership=True) == [p_b]
    assert intersect(patient, user, user_membership=True) == [u_b]
    assert intersect(patient, user, patient_membership=True, user_membership=True) == [(p_b, u_b)]


def make_patient(organisations=None):
    if organisations is None:
        organisations = []

    patient = Patient()

    for organisation in organisations:
        organisation_patient = OrganisationPatient()
        organisation_patient.organisation = organisation
        organisation_patient.patient = patient
        patient.organisation_patients.append(organisation_patient)

    return patient


def make_user(organisations=None):
    if organisations is None:
        organisations = []

    user = User()

    for organisation in organisations:
        organisation_user = OrganisationUser()
        organisation_user.organisation = organisation
        organisation_user.user = user
        user.organisation_users.append(organisation_user)

    return user


def make_organisations(n):
    return [Organisation() for _ in range(n)]

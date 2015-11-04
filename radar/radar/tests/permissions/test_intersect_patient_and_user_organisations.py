from radar.permissions import intersect_patient_and_user_organisations as intersect_organisations
from radar.tests.helpers.permissions import make_patient, make_user, make_organisations


def test_empty():
    patient = make_patient()
    user = make_user()

    assert intersect_organisations(patient, user) == []
    assert intersect_organisations(patient, user, patient_membership=True) == []
    assert intersect_organisations(patient, user, user_membership=True) == []
    assert intersect_organisations(patient, user, patient_membership=True, user_membership=True) == []


def test_intersecting():
    a, b, c, d = make_organisations(4)

    patient = make_patient(organisations=[a, b, c])
    p_a, p_b, p_c = patient.organisation_patients

    user = make_user(organisations=[b, c, d])
    u_b, u_c, u_d = user.organisation_users

    assert intersect_organisations(patient, user) == [b, c]
    assert intersect_organisations(patient, user, patient_membership=True) == [p_b, p_c]
    assert intersect_organisations(patient, user, user_membership=True) == [u_b, u_c]
    assert intersect_organisations(patient, user, patient_membership=True, user_membership=True) == [
        (p_b, u_b),
        (p_c, u_c),
    ]


def test_disjoint():
    a, b, c, d = make_organisations(4)

    patient = make_patient(organisations=[a, b])
    p_a, p_b = patient.organisation_patients

    user = make_user(organisations=[c, d])
    u_c, u_d = user.organisation_users

    assert intersect_organisations(patient, user) == []
    assert intersect_organisations(patient, user, patient_membership=True) == []
    assert intersect_organisations(patient, user, user_membership=True) == []
    assert intersect_organisations(patient, user, patient_membership=True, user_membership=True) == []


def test_admin():
    a, b, c = make_organisations(3)

    patient = make_patient(organisations=[a, b])
    p_a, p_b = patient.organisation_patients

    user = make_user(organisations=[b, c])
    user.is_admin = True
    u_b, u_c = user.organisation_users

    assert intersect_organisations(patient, user) == [b]
    assert intersect_organisations(patient, user, patient_membership=True) == [p_b]
    assert intersect_organisations(patient, user, user_membership=True) == [u_b]
    assert intersect_organisations(patient, user, patient_membership=True, user_membership=True) == [(p_b, u_b)]

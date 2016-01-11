from radar.permissions import intersect_patient_and_user_groups
from radar.tests.permissions.helpers import make_patient, make_user, make_groups


def test_empty():
    patient = make_patient()
    user = make_user()

    assert intersect_patient_and_user_groups(patient, user) == []
    assert intersect_patient_and_user_groups(patient, user, patient_membership=True) == []
    assert intersect_patient_and_user_groups(patient, user, user_membership=True) == []
    assert intersect_patient_and_user_groups(patient, user, patient_membership=True, user_membership=True) == []


def test_intersecting():
    a, b, c, d = make_groups(4)

    patient = make_patient([a, b, c])
    p_a, p_b, p_c = patient.group_patients

    user = make_user([b, c, d])
    u_b, u_c, u_d = user.group_users

    assert intersect_patient_and_user_groups(patient, user) == [b, c]
    assert intersect_patient_and_user_groups(patient, user, patient_membership=True) == [p_b, p_c]
    assert intersect_patient_and_user_groups(patient, user, user_membership=True) == [u_b, u_c]
    assert intersect_patient_and_user_groups(patient, user, patient_membership=True, user_membership=True) == [
        (p_b, u_b),
        (p_c, u_c),
    ]


def test_disjoint():
    a, b, c, d = make_groups(4)

    patient = make_patient([a, b])
    p_a, p_b = patient.group_patients

    user = make_user([c, d])
    u_c, u_d = user.group_users

    assert intersect_patient_and_user_groups(patient, user) == []
    assert intersect_patient_and_user_groups(patient, user, patient_membership=True) == []
    assert intersect_patient_and_user_groups(patient, user, user_membership=True) == []
    assert intersect_patient_and_user_groups(patient, user, patient_membership=True, user_membership=True) == []


def test_admin():
    a, b, c = make_groups(3)

    patient = make_patient([a, b])
    p_a, p_b = patient.group_patients

    user = make_user([b, c])
    user.is_admin = True
    u_b, u_c = user.group_users

    assert intersect_patient_and_user_groups(patient, user) == [b]
    assert intersect_patient_and_user_groups(patient, user, patient_membership=True) == [p_b]
    assert intersect_patient_and_user_groups(patient, user, user_membership=True) == [u_b]
    assert intersect_patient_and_user_groups(patient, user, patient_membership=True, user_membership=True) == [(p_b, u_b)]

from radar.permissions import intersect_groups_with_patient
from tests.permissions.helpers import make_groups, make_patient, make_user


def test_empty():
    patient = make_patient()
    user = make_user()

    assert intersect_groups_with_patient(user, patient) == []
    assert intersect_groups_with_patient(user, patient, patient_membership=True) == []
    assert intersect_groups_with_patient(user, patient, patient_membership=True) == []
    assert intersect_groups_with_patient(user, patient, user_membership=True, patient_membership=True) == []


def test_intersecting():
    a, b, c, d = make_groups(4)

    patient = make_patient([a, b, c])
    p_a, p_b, p_c = patient.group_patients

    user = make_user([b, c, d])
    print user.group_users
    u_b, u_c, u_d = user.group_users

    assert intersect_groups_with_patient(user, patient) == [b, c]
    assert intersect_groups_with_patient(user, patient, user_membership=True) == [u_b, u_c]
    assert intersect_groups_with_patient(user, patient, patient_membership=True) == [p_b, p_c]
    assert intersect_groups_with_patient(user, patient, user_membership=True, patient_membership=True) == [
        (u_b, p_b),
        (u_c, p_c),
    ]


def test_disjoint():
    a, b, c, d = make_groups(4)

    patient = make_patient([a, b])
    p_a, p_b = patient.group_patients

    user = make_user([c, d])
    u_c, u_d = user.group_users

    assert intersect_groups_with_patient(user, patient) == []
    assert intersect_groups_with_patient(user, patient, user_membership=True) == []
    assert intersect_groups_with_patient(user, patient, patient_membership=True) == []
    assert intersect_groups_with_patient(user, patient, user_membership=True, patient_membership=True) == []


def test_admin():
    a, b, c = make_groups(3)

    patient = make_patient([a, b])
    p_a, p_b = patient.group_patients

    user = make_user([b, c])
    user.is_admin = True
    u_b, u_c = user.group_users

    assert intersect_groups_with_patient(user, patient) == [b]
    assert intersect_groups_with_patient(user, patient, user_membership=True) == [u_b]
    assert intersect_groups_with_patient(user, patient, patient_membership=True) == [p_b]
    assert intersect_groups_with_patient(user, patient, user_membership=True, patient_membership=True) == [(u_b, p_b)]

from radar.permissions import intersect_patient_and_user_cohorts as intersect_cohorts
from helpers.permissions import make_patient, make_user, make_cohorts


def test_empty():
    patient = make_patient()
    user = make_user()

    assert intersect_cohorts(patient, user) == []
    assert intersect_cohorts(patient, user, patient_membership=True) == []
    assert intersect_cohorts(patient, user, user_membership=True) == []
    assert intersect_cohorts(patient, user, patient_membership=True, user_membership=True) == []


def test_intersecting():
    a, b, c, d = make_cohorts(4)

    patient = make_patient(cohorts=[a, b, c])
    p_a, p_b, p_c = patient.cohort_patients

    user = make_user(cohorts=[b, c, d])
    u_b, u_c, u_d = user.cohort_users

    assert intersect_cohorts(patient, user) == [b, c]
    assert intersect_cohorts(patient, user, patient_membership=True) == [p_b, p_c]
    assert intersect_cohorts(patient, user, user_membership=True) == [u_b, u_c]
    assert intersect_cohorts(patient, user, patient_membership=True, user_membership=True) == [
        (p_b, u_b),
        (p_c, u_c),
    ]


def test_disjoint():
    a, b, c, d = make_cohorts(4)

    patient = make_patient(cohorts=[a, b])
    p_a, p_b = patient.cohort_patients

    user = make_user(cohorts=[c, d])
    u_c, u_d = user.cohort_users

    assert intersect_cohorts(patient, user) == []
    assert intersect_cohorts(patient, user, patient_membership=True) == []
    assert intersect_cohorts(patient, user, user_membership=True) == []
    assert intersect_cohorts(patient, user, patient_membership=True, user_membership=True) == []


def test_admin():
    a, b, c = make_cohorts(3)

    patient = make_patient(cohorts=[a, b])
    p_a, p_b = patient.cohort_patients

    user = make_user(cohorts=[b, c])
    user.is_admin = True
    u_b, u_c = user.cohort_users

    assert intersect_cohorts(patient, user) == [b]
    assert intersect_cohorts(patient, user, patient_membership=True) == [p_b]
    assert intersect_cohorts(patient, user, user_membership=True) == [u_b]
    assert intersect_cohorts(patient, user, patient_membership=True, user_membership=True) == [(p_b, u_b)]

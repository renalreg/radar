from radar.permissions import intersect_patient_and_user_cohorts as intersect
from radar.models.patients import Patient
from radar.models.users import User
from radar.models.cohorts import Cohort, CohortUser, CohortPatient


def test_empty():
    patient = make_patient()
    user = make_user()

    assert intersect(patient, user) == []
    assert intersect(patient, user, patient_membership=True) == []
    assert intersect(patient, user, user_membership=True) == []
    assert intersect(patient, user, patient_membership=True, user_membership=True) == []


def test_intersection():
    a, b, c, d = make_cohorts(4)

    patient = make_patient([a, b, c])
    p_a, p_b, p_c = patient.cohort_patients

    user = make_user([b, c, d])
    u_b, u_c, u_d = user.cohort_users

    assert intersect(patient, user) == [b, c]
    assert intersect(patient, user, patient_membership=True) == [p_b, p_c]
    assert intersect(patient, user, user_membership=True) == [u_b, u_c]
    assert intersect(patient, user, patient_membership=True, user_membership=True) == [
        (p_b, u_b),
        (p_c, u_c),
    ]


def test_disjoint():
    a, b, c, d = make_cohorts(4)

    patient = make_patient([a, b])
    p_a, p_b = patient.cohort_patients

    user = make_user([c, d])
    u_c, u_d = user.cohort_users

    assert intersect(patient, user) == []
    assert intersect(patient, user, patient_membership=True) == []
    assert intersect(patient, user, user_membership=True) == []
    assert intersect(patient, user, patient_membership=True, user_membership=True) == []


def test_admin():
    a, b, c = make_cohorts(3)

    patient = make_patient([a, b])
    p_a, p_b = patient.cohort_patients

    user = make_user([b, c])
    user.is_admin = True
    u_b, u_c = user.cohort_users

    assert intersect(patient, user) == [b]
    assert intersect(patient, user, patient_membership=True) == [p_b]
    assert intersect(patient, user, user_membership=True) == [u_b]
    assert intersect(patient, user, patient_membership=True, user_membership=True) == [(p_b, u_b)]


def make_patient(cohorts=None):
    if cohorts is None:
        cohorts = []

    patient = Patient()

    for cohort in cohorts:
        cohort_patient = CohortPatient()
        cohort_patient.cohort = cohort
        cohort_patient.patient = patient
        patient.cohort_patients.append(cohort_patient)

    return patient


def make_user(cohorts=None):
    if cohorts is None:
        cohorts = []

    user = User()

    for cohort in cohorts:
        cohort_user = CohortUser()
        cohort_user.cohort = cohort
        cohort_user.user = user
        user.cohort_users.append(cohort_user)

    return user


def make_cohorts(n):
    return [Cohort() for _ in range(n)]

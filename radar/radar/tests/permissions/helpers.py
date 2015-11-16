from radar.models.cohorts import Cohort, CohortPatient, CohortUser
from radar.models.organisations import Organisation, OrganisationPatient, OrganisationUser
from radar.models.patients import Patient
from radar.models.users import User
from radar.permissions import Permission


class MockRequest(object):
    def __init__(self, method):
        self.method = method


class MockPermission(Permission):
    def __init__(self):
        self.has_permission_called = False
        self.has_object_permission_called = False

    def has_permission(self, request, user):
        self.has_permission_called = True
        return True

    def has_object_permission(self, request, user, obj):
        self.has_object_permission_called = True
        return True


def make_cohorts(n):
    return [Cohort() for _ in range(n)]


def make_organisations(n):
    return [Organisation() for _ in range(n)]


def make_patient(organisations=None, cohorts=None):
    if organisations is None:
        organisations = []

    if cohorts is None:
        cohorts = []

    patient = Patient()

    for organisation in organisations:
        organisation_patient = OrganisationPatient()
        organisation_patient.organisation = organisation
        organisation_patient.patient = patient

    for cohort in cohorts:
        cohort_patient = CohortPatient()
        cohort_patient.cohort = cohort
        cohort_patient.patient = patient

    return patient


def make_user(organisations=None, cohorts=None):
    if organisations is None:
        organisations = []

    if cohorts is None:
        cohorts = []

    user = User()

    for organisation in organisations:
        if isinstance(organisation, OrganisationUser):
            organisation_user = organisation
        else:
            try:
                organisation, role = organisation
            except (TypeError, ValueError):
                role = None

            organisation_user = OrganisationUser()
            organisation_user.organisation = organisation
            organisation_user.user = user
            organisation_user.role = role

        user.organisation_users.append(organisation_user)

    for cohort in cohorts:
        if isinstance(cohort, CohortUser):
            cohort_user = cohort
        else:
            try:
                cohort, role = cohort
            except (TypeError, ValueError):
                role = None

            cohort_user = CohortUser()
            cohort_user.cohort = cohort
            cohort_user.user = user
            cohort_user.role = role

        user.cohort_users.append(cohort_user)

    return user

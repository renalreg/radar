from sqlalchemy import or_, case, desc, extract

from sqlalchemy.orm import aliased, subqueryload
from radar.models import PatientAlias, PatientNumber
from radar.roles import get_cohort_roles_with_permission, get_organisation_roles_with_permission, PERMISSIONS
from radar.database import db
from radar.models.organisations import OrganisationPatient, Organisation, OrganisationUser
from radar.models.cohorts import Cohort, CohortPatient, CohortUser
from radar.models.patients import Patient, PatientDemographics
from radar.utils import sql_year_filter, sql_date_filter


class PatientQueryBuilder(object):
    def __init__(self, current_user):
        self.current_user = current_user

        # True if the query is filtering on demographics
        self.filtering_by_demographics = False

        self.query = Patient.query\
            .options(subqueryload('patient_demographics'))\
            .options(subqueryload('organisation_patients').joinedload('organisation'))\
            .options(subqueryload('cohort_patients').joinedload('cohort'))

    def first_name(self, first_name):
        self.filtering_by_demographics = True
        self.query = self.query.filter(filter_by_first_name(first_name))
        return self

    def last_name(self, last_name):
        self.filtering_by_demographics = True
        self.query = self.query.filter(filter_by_last_name(last_name))
        return self

    def gender(self, gender):
        self.query = self.query.filter(filter_by_gender(gender))
        return self

    def patient_number(self, patient_number):
        self.filtering_by_demographics = True
        self.query = self.query.filter(filter_by_patient_number(patient_number))
        return self

    def patient_id(self, radar_id):
        self.query = self.query.filter(filter_by_patient_id(radar_id))
        return self

    def date_of_birth(self, value):
        self.filtering_by_demographics = True
        self.query = self.query.filter(filter_by_date_of_birth(value))
        return self

    def year_of_birth(self, value):
        self.query = self.query.filter(filter_by_year_of_birth(value))
        return self

    def date_of_death(self, value):
        self.filtering_by_demographics = True
        self.query = self.query.filter(filter_by_date_of_death(value))
        return self

    def year_of_death(self, value):
        self.query = self.query.filter(filter_by_year_of_death(value))
        return self

    def organisation(self, organisation, is_active=None):
        self.query = self.query\
            .join(OrganisationPatient)\
            .filter(OrganisationPatient.organisation == organisation)

        if is_active is not None:
            self.query = self.query.filter(OrganisationPatient.is_active == is_active)

        return self

    def cohort(self, cohort, is_active=None):
        # Filter by cohort
        self.query = self.query\
            .join(CohortPatient)\
            .filter(CohortPatient.cohort == cohort)

        if is_active is not None:
            self.query = self.query.filter(CohortPatient.is_active == is_active)

        return self

    def is_active(self, is_active):
        self.query = self.query.filter(Patient.is_active == is_active)
        return self

    def sort(self, column, reverse=False):
        self.query = self.query.order_by(*sort_patients(self.current_user, column, reverse))

    def build(self, apply_permissions=True):
        query = self.query

        # TODO check is_active here

        if apply_permissions and not self.current_user.is_admin:
            # Filter the patients based on the user's permissions and the type of query
            permission_filter = filter_by_permissions(self.current_user, self.filtering_by_demographics)
            query = query.filter(permission_filter)

        return query


def patient_demographics_sub_query(*args):
    patient_alias = aliased(Patient)
    sub_query = db.session.query(PatientDemographics)\
        .join(patient_alias)\
        .filter(Patient.id == patient_alias.id)\
        .filter(*args)\
        .exists()
    return sub_query


def patient_alias_sub_query(*args):
    patient_alias = aliased(Patient)
    sub_query = db.session.query(PatientAlias)\
        .join(patient_alias)\
        .filter(Patient.id == patient_alias.id)\
        .filter(*args)\
        .exists()
    return sub_query


def patient_number_sub_query(*args):
    patient_alias = aliased(Patient)
    sub_query = db.session.query(PatientNumber)\
        .join(patient_alias)\
        .filter(Patient.id == patient_alias.id)\
        .filter(*args)\
        .exists()
    return sub_query


def filter_by_first_name(first_name):
    # Prefix search
    first_name_like = first_name + '%'
    patient_filter = patient_demographics_sub_query(PatientDemographics.first_name.ilike(first_name_like))
    alias_filter = patient_alias_sub_query(PatientAlias.first_name.ilike(first_name_like))
    return or_(patient_filter, alias_filter)


def filter_by_last_name(last_name):
    # Prefix search
    last_name_like = last_name + '%'
    patient_filter = patient_demographics_sub_query(PatientDemographics.last_name.ilike(last_name_like))
    alias_filter = patient_alias_sub_query(PatientAlias.last_name.ilike(last_name_like))
    return or_(patient_filter, alias_filter)


def filter_by_date_of_birth(date_of_birth):
    return patient_demographics_sub_query(sql_date_filter(PatientDemographics.date_of_birth, date_of_birth))


def filter_by_date_of_death(date_of_death):
    return patient_demographics_sub_query(sql_date_filter(PatientDemographics.date_of_death, date_of_death))


def filter_by_patient_number(number, exact=False):
    if exact:
        query = patient_number_sub_query(PatientNumber.number.like(number + '%'))
    else:
        query = patient_number_sub_query(PatientNumber.number == number)

    try:
        # Also search RaDaR IDs
        query = or_(query, filter_by_patient_id(int(number)))
    except ValueError:
        pass

    return query


def filter_by_patient_number_at_organisation(number, organisation, exact=False):
    if exact:
        query = patient_number_sub_query(PatientNumber.number.like(number + '%'), PatientNumber.organisation == organisation)
    else:
        query = patient_number_sub_query(PatientNumber.number == number, PatientNumber.organisation == organisation)

    return query


def filter_by_patient_id(patient_id):
    return Patient.id == patient_id


def filter_by_gender(gender_code):
    return patient_demographics_sub_query(PatientDemographics.gender == gender_code)


def filter_by_year_of_birth(year):
    return patient_demographics_sub_query(sql_year_filter(PatientDemographics.date_of_birth, year))


def filter_by_year_of_death(year):
    return patient_demographics_sub_query(sql_year_filter(PatientDemographics.date_of_death, year))


def filter_by_organisation_roles(current_user, roles):
    patient_alias = aliased(Patient)
    sub_query = db.session.query(patient_alias)\
        .join(patient_alias.organisation_patients)\
        .join(OrganisationPatient.organisation)\
        .join(Organisation.organisation_users)\
        .filter(
            patient_alias.id == Patient.id,
            OrganisationUser.user_id == current_user.id,
            OrganisationUser.role.in_(roles)
        )\
        .exists()
    return sub_query


def filter_by_cohort_roles(current_user, roles):
    patient_alias = aliased(Patient)
    sub_query = db.session.query(patient_alias)\
        .join(patient_alias.cohort_patients)\
        .join(CohortPatient.cohort)\
        .join(Cohort.cohort_users)\
        .filter(
            patient_alias.id == Patient.id,
            CohortUser.user_id == current_user.id,
            CohortUser.role.in_(roles)
        )\
        .exists()
    return sub_query


def filter_by_permissions(current_user, demographics):
    if demographics:
        return or_(
            filter_by_organisation_roles(current_user, get_organisation_roles_with_permission(PERMISSIONS.VIEW_DEMOGRAPHICS)),
            filter_by_cohort_roles(current_user, get_cohort_roles_with_permission(PERMISSIONS.VIEW_DEMOGRAPHICS)),
        )
    else:
        return or_(
            filter_by_organisation_roles(current_user, get_organisation_roles_with_permission(PERMISSIONS.VIEW_PATIENT)),
            filter_by_cohort_roles(current_user, get_cohort_roles_with_permission(PERMISSIONS.VIEW_PATIENT)),
        )


def sort_by_demographics_field(current_user, field, reverse, else_=None):
    if current_user.is_admin:
        expression = field
    else:
        demographics_permission_sub_query = or_(
            filter_by_organisation_roles(current_user, get_organisation_roles_with_permission(PERMISSIONS.VIEW_DEMOGRAPHICS)),
            filter_by_cohort_roles(current_user, get_cohort_roles_with_permission(PERMISSIONS.VIEW_DEMOGRAPHICS)),
        )
        expression = case([(demographics_permission_sub_query, field)], else_=else_)

    if reverse:
        expression = desc(expression)

    return expression


def sort_by_field(field, reverse=False):
    if reverse:
        field = desc(field)

    return field


def sort_by_radar_id(reverse=False):
    return sort_by_field(Patient.id, reverse)


def sort_by_first_name(current_user, reverse=False):
    return sort_by_demographics_field(current_user, Patient.first_name, reverse)


def sort_by_last_name(current_user, reverse=False):
    return sort_by_demographics_field(current_user, Patient.last_name, reverse)


def sort_by_gender(reverse=False):
    return sort_by_field(Patient.gender, reverse)


def sort_by_date_of_birth(current_user, reverse=False):
    date_of_birth_order = sort_by_demographics_field(current_user, Patient.date_of_birth, reverse)

    if current_user.is_admin:
        return [date_of_birth_order]
    else:
        # Users without demographics permissions can only see the year
        year_order = sort_by_field(extract('year', Patient.date_of_birth), reverse)

        # Anonymised (year) values first (i.e. treat 1999 as 1999-01-01)
        anonymised_order = sort_by_demographics_field(current_user, 1, reverse, else_=0)

        return [year_order, anonymised_order, date_of_birth_order]


def sort_by_recruited_date(reverse=False):
    return sort_by_field(Patient.recruited_date, reverse)


def sort_patients(user, sort_by, reverse=False):
    if sort_by == 'first_name':
        clauses = [sort_by_first_name(user, reverse)]
    elif sort_by == 'last_name':
        clauses = [sort_by_last_name(user, reverse)]
    elif sort_by == 'gender':
        clauses = [sort_by_gender(reverse)]
    elif sort_by == 'date_of_birth':
        clauses = sort_by_date_of_birth(user, reverse)
    elif sort_by == 'recruited_date':
        clauses = [sort_by_recruited_date(reverse)]
    else:
        return [sort_by_radar_id(reverse)]

    # Decide ties using RaDaR ID
    clauses.append(sort_by_radar_id())

    return clauses

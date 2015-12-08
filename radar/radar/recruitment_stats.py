from datetime import datetime

from sqlalchemy import cast, extract, Integer, func
from sqlalchemy.sql.expression import null, distinct

from radar.database import db
from radar.models.cohorts import CohortPatient, Cohort
from radar.models.patients import Patient
from radar.models.organisations import OrganisationPatient, Organisation


def recruitment_by_month(date_column, filters=None):
    year_column = cast(extract('year', date_column), Integer)
    month_column = cast(extract('month', date_column), Integer)

    query = db.session\
        .query(year_column, month_column, func.count())\
        .filter(date_column != null())\
        .group_by(year_column, month_column)\
        .order_by(year_column, month_column)

    if filters is not None:
        query = query.filter(*filters)

    data = {(year, month): count for year, month, count in query.all()}

    if not data:
        return []

    current_year, current_month = min(data.keys())
    last_year, last_month = max(data.keys())

    total = 0
    results = []

    while current_year < last_year or (current_year == last_year and current_month <= last_month):
        count = data.get((current_year, current_month), 0)
        total += count

        results.append({'date': datetime(current_year, current_month, 1), 'newPatients': count, 'totalPatients': total})

        if current_month == 12:
            current_year += 1
            current_month = 1
        else:
            current_month += 1

    return results


def recruitment_by_cohort(filters=None):
    return recruitment_by_group(Cohort, CohortPatient.cohort_id, filters)


def recruitment_by_organisation(filters=None):
    return recruitment_by_group(Organisation, OrganisationPatient.organisation_id, filters)


def recruitment_by_group(model, group_column, filters=None):
    count_query = db.session.query(group_column.label('id'), func.count(distinct(Patient.id)).label('patient_count'))\
        .select_from(Patient)\
        .join(CohortPatient)\
        .join(OrganisationPatient)\
        .group_by(group_column)

    if filters is not None:
        count_query = count_query.filter(*filters)

    count_subquery = count_query.subquery()

    query = db.session\
        .query(model, count_subquery.c.patient_count)\
        .outerjoin(count_subquery, model.id == count_subquery.c.id)\
        .filter(count_subquery.c.patient_count > 0)\
        .order_by(model.id)

    return query.all()

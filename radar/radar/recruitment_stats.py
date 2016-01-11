from datetime import datetime

from sqlalchemy import cast, extract, Integer, func
from sqlalchemy.sql.expression import null, distinct
from sqlalchemy.orm import aliased

from radar.database import db
from radar.models.groups import GroupPatient, Group
from radar.models.patients import Patient


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


def recruitment_by_group(group=None, group_type=None):
    count_query = db.session.query(GroupPatient.group_id.label('group_id'), func.count(distinct(Patient.id)).label('patient_count'))\
        .select_from(Patient)\
        .join(Patient.group_patients)\
        .join(GroupPatient.group)\
        .group_by(GroupPatient.group_id)

    # Filter by patients belonging to the specified group
    if group is not None:
        patient_alias = aliased(Patient)
        group_subquery = db.session.query(patient_alias)\
            .join(patient_alias.group_patients)\
            .filter(
                patient_alias.id == Patient.id,
                GroupPatient.group == group,
            )\
            .exists()

        count_query = count_query.filter(group_subquery)
        count_query = count_query.filter(GroupPatient.group != group)

    # Filter by groups of a particular type
    if group_type is not None:
        count_query = count_query.filter(Group.type == group_type)

    count_subquery = count_query.subquery()

    query = db.session\
        .query(Group, count_subquery.c.patient_count)\
        .join(count_subquery, Group.id == count_subquery.c.group_id)\
        .order_by(Group.id)

    return query.all()

from datetime import datetime

from sqlalchemy import cast, extract, Integer, func
from sqlalchemy.sql.expression import distinct
from sqlalchemy.orm import aliased

from radar.database import db
from radar.models.groups import GroupPatient, Group
from radar.models.patients import Patient


def recruitment_by_month(group):
    """
    Calculate the number of patients recruited each month to the
    specified group.
    """

    # Earliest from date for each patient for this group.
    # It's possible for a patient to have multiple membership records.
    # For example a patient may withdraw their consent and then later re-consent.
    q1 = db.session.query(func.min(GroupPatient.from_date).label('from_date'))\
        .filter(GroupPatient.group_id == group.id)\
        .group_by(GroupPatient.patient_id)\
        .subquery()

    # Extract the year and month from the from date.
    year_column = cast(extract('year', q1.c.from_date), Integer)
    month_column = cast(extract('month', q1.c.from_date), Integer)

    # Aggregate results by month.
    q2 = db.session.query(year_column, month_column, func.count())\
        .group_by(year_column, month_column)\
        .order_by(year_column, month_column)

    # Convert the results into a map indexed by month.
    data = {(year, month): count for year, month, count in q2.all()}

    # No patients recruited.
    # Exit early as min/max will fail on an empty list.
    if not data:
        return []

    # Find the earliest and latest months where a patient was recuited.
    current_year, current_month = min(data.keys())
    last_year, last_month = max(data.keys())

    # Keep a running total of the number of patients recruited.
    total = 0
    results = []

    # Fill in gaps (months where no patients were recruited) and calculate
    # cumulative totals.
    while current_year < last_year or (current_year == last_year and current_month <= last_month):
        count = data.get((current_year, current_month), 0)
        total += count

        results.append({
            'date': datetime(current_year, current_month, 1),
            'new_patients': count,
            'total_patients': total
        })

        # Move to the next month.
        if current_month == 12:
            current_year += 1
            current_month = 1
        else:
            current_month += 1

    return results


def patients_by_group(group=None, group_type=None):
    count_query = db.session.query(
        GroupPatient.group_id.label('group_id'),
        func.count(distinct(Patient.id)).label('patient_count')
    )
    count_query = count_query.select_from(Patient)
    count_query = count_query.join(Patient.group_patients)
    count_query = count_query.group_by(GroupPatient.group_id)

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

    count_subquery = count_query.subquery()

    query = db.session\
        .query(Group, count_subquery.c.patient_count)\
        .join(count_subquery, Group.id == count_subquery.c.group_id)\
        .order_by(Group.id)

    # Filter by groups of a particular type
    if group_type is not None:
        query = query.filter(Group.type == group_type)

    return query.all()


def patients_by_recruited_group(group):
    """
    Calculate the number of patients each group has recruited to
    the specified group.

    The recruiting group is the first group to add the patient to
    the group we're querying. In practice this is the membership record
    with the earliest from date.
    """

    # Use a window function to find the group that recruited each
    # patient. The recruiting group is the group that created the
    # earliest membership record (determined by from date). The query
    # is filtered by the specified group and the distinct clause ensures
    # we only get one result per patient.
    first_created_group_id_column = func.first_value(GroupPatient.created_group_id)\
        .over(partition_by=GroupPatient.patient_id, order_by=GroupPatient.from_date)\
        .label('created_group_id')
    q1 = db.session.query(first_created_group_id_column)\
        .distinct(GroupPatient.patient_id)\
        .filter(GroupPatient.group_id == group.id)\
        .subquery()

    # Aggregate the results by recruiting group to get the number of
    # patients recruited by each group.
    created_group_id_column = q1.c.created_group_id.label('created_group_id')
    patient_count_column = func.count().label('patient_count')
    q2 = db.session.query(created_group_id_column, patient_count_column)\
        .group_by(created_group_id_column)\
        .subquery()

    # Join the results with the groups table.
    q3 = db.session.query(Group, q2.c.patient_count)\
        .join(q2, Group.id == q2.c.created_group_id)\
        .order_by(Group.id)

    return q3.all()

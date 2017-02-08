from datetime import datetime

from sqlalchemy import and_, cast, extract, func, Integer, text
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import distinct, false, true

from radar.database import db
from radar.models.groups import Group, GROUP_TYPE, GroupPatient
from radar.models.patients import Patient


def patients_by_recruitment_date(group, interval='month'):
    """
    Calculate the number of patients recruited each month to the
    specified group.
    """

    # Earliest from date for each patient for this group.
    # It's possible for a patient to have multiple membership records.
    # For example a patient may withdraw their consent and then later re-consent.
    q1 = db.session.query(func.min(GroupPatient.from_date).label('from_date'))
    q1 = q1.filter(GroupPatient.group_id == group.id)
    q1 = q1.join(GroupPatient.patient)
    q1 = q1.filter(Patient.test == false())

    if group.type == GROUP_TYPE.SYSTEM:
        q1 = q1.filter(Patient.current(group) == true())
    else:
        q1 = q1.filter(Patient.current() == true())

    q1 = q1.group_by(GroupPatient.patient_id)
    q1 = q1.subquery()

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

        # Reached end of the current year
        if current_month == 12:
            # Wrap around
            current_year += 1
            current_month = 1
        else:
            # Next month
            current_month += 1

    return results


def patients_by_group(group=None, group_type=None):
    """
    Calculate the number of patients in each group.

    Optionally specify a group to only include patients that
    are a member of that group.

    You can also specify a group type so only groups of that
    type are included in the results.
    """

    # Count the number of distinct patients in each group. Patients can have
    # multiple memberships for each group but should only be counted once.
    count_query = db.session.query(
        GroupPatient.group_id.label('group_id'),
        func.count(distinct(Patient.id)).label('patient_count')
    )
    count_query = count_query.select_from(Patient)
    count_query = count_query.join(Patient.group_patients)
    count_query = count_query.filter(Patient.test == false())

    if group is not None and group.type == GROUP_TYPE.SYSTEM:
        count_query = count_query.filter(Patient.current(group) == true())
    else:
        count_query = count_query.filter(Patient.current() == true())

    count_query = count_query.group_by(GroupPatient.group_id)

    # Filter the results to only include patients belonging to the
    # specified group.
    if group is not None:
        patient_alias = aliased(Patient)
        group_subquery = db.session.query(patient_alias)
        group_subquery = group_subquery.join(patient_alias.group_patients)
        group_subquery = group_subquery.filter(
            patient_alias.id == Patient.id,
            GroupPatient.group == group,
        )
        group_subquery = group_subquery.exists()

        count_query = count_query.filter(group_subquery)

        # We are only interested in groups other than the specified
        # group so exclude it from the results.
        count_query = count_query.filter(GroupPatient.group != group)

    count_subquery = count_query.subquery()

    # Join the results with the groups table.
    query = db.session\
        .query(Group, count_subquery.c.patient_count)\
        .join(count_subquery, Group.id == count_subquery.c.group_id)\
        .order_by(Group.id)

    # Filter the results to only include groups of the specified
    # type (e.g. COHORT). By default all group types are included.
    if group_type is not None:
        query = query.filter(Group.type == group_type)

    return query.all()


def patients_by_recruitment_group(group):
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
    q1 = db.session.query(first_created_group_id_column)
    q1 = q1.distinct(GroupPatient.patient_id)
    q1 = q1.join(GroupPatient.patient)
    q1 = q1.filter(GroupPatient.group_id == group.id)
    q1 = q1.filter(Patient.test == false())

    if group.type == GROUP_TYPE.SYSTEM:
        q1 = q1.filter(Patient.current(group) == true())
    else:
        q1 = q1.filter(Patient.current() == true())

    q1 = q1.subquery()

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


def patients_by_group_date(group=None, group_type=None, interval='month'):
    """
    Number of patients in each group over time.
    """

    query = db.session.query(
        GroupPatient.group_id,
        GroupPatient.patient_id,
        func.min(GroupPatient.from_date).label('date')
    )
    query = query.join(GroupPatient.patient)
    query = query.filter(Patient.test == false())

    if group is not None and group.type == 'SYSTEM':
        query = query.filter(Patient.current(group) == true())
    else:
        query = query.filter(Patient.current() == true())

    # Filter by patients beloning to the specified group
    if group is not None:
        patient_alias = aliased(Patient)
        group_subquery = db.session.query(patient_alias)
        group_subquery = group_subquery.join(patient_alias.group_patients)
        group_subquery = group_subquery.filter(
            patient_alias.id == Patient.id,
            GroupPatient.group == group,
        )
        group_subquery = group_subquery.exists()

        query = query.filter(group_subquery)

    # Filter by group type
    if group_type is not None:
        query = query.join(GroupPatient.group)
        query = query.filter(Group.type == group_type)

    query = query.group_by(GroupPatient.group_id, GroupPatient.patient_id)
    query = query.cte()

    results = _get_results(query, interval)

    return results


def patients_by_recruitment_group_date(group, interval='month'):
    """
    Number of patients recruited by each group over time.
    """

    group_id_c = func.first_value(GroupPatient.created_group_id)\
        .over(partition_by=GroupPatient.patient_id, order_by=GroupPatient.from_date)\
        .label('group_id')
    date_c = func.min(GroupPatient.from_date)\
        .over(partition_by=GroupPatient.patient_id)\
        .label('date')

    query = db.session.query(GroupPatient.patient_id, group_id_c, date_c)
    query = query.distinct()
    query = query.join(GroupPatient.patient)
    query = query.filter(GroupPatient.group_id == group.id)
    query = query.filter(Patient.test == false())

    if group.type == GROUP_TYPE.SYSTEM:
        query = query.filter(Patient.current(group) == true())
    else:
        query = query.filter(Patient.current() == true())

    query = query.cte()

    results = _get_results(query, interval)

    return results


def _to_month(column):
    return func.make_date(cast(extract('year', column), Integer), cast(extract('month', column), Integer), 1)


def _get_months(query):
    min_ = _to_month(func.min(query.c.date))
    max_ = _to_month(func.max(query.c.date))
    age = func.age(max_, min_)
    n = cast(extract('year', age) * 12 + extract('month', age), Integer)
    q = db.session.query((min_ + text("interval '1' month") * func.generate_series(0, n)).label('date'))
    return q


def _get_groups(query):
    return db.session.query(distinct(query.c.group_id).label('group_id'))


def _get_buckets(query, interval='month'):
    q1 = _get_groups(query).cte()
    q2 = _get_months(query).cte()
    q3 = db.session.query(q1.c.group_id, q2.c.date).cte()
    return q3


def _get_results(query, interval='month'):
    buckets_q = _get_buckets(query, interval)

    counts_q = db.session.query(
        query.c.group_id,
        _to_month(query.c.date).label('date'),
        func.count(query.c.patient_id).label('count')
    )
    counts_q = counts_q.group_by(query.c.group_id, _to_month(query.c.date))
    counts_q = counts_q.cte()

    new_c = func.coalesce(counts_q.c.count, 0).label('new')
    total_c = func.coalesce(
        func.sum(counts_q.c.count).over(
            partition_by=buckets_q.c.group_id,
            order_by=buckets_q.c.date), 0).label('total')

    timeline_q = db.session.query(buckets_q.c.group_id, buckets_q.c.date, new_c, total_c)
    timeline_q = timeline_q.select_from(buckets_q)
    timeline_q = timeline_q.outerjoin(
        counts_q,
        and_(buckets_q.c.group_id == counts_q.c.group_id, buckets_q.c.date == counts_q.c.date))
    timeline_q = timeline_q.cte()

    results_q = db.session.query(Group, timeline_q.c.date, timeline_q.c.new, timeline_q.c.total)
    results_q = results_q.join(timeline_q, Group.id == timeline_q.c.group_id)
    results_q = results_q.order_by(Group.id, timeline_q.c.date)

    results = []
    groups = {}

    for group, date, new_patients, total_patients in results_q.all():
        result = groups.get(group)

        if result is None:
            result = {'group': group, 'counts': []}
            results.append(result)
            groups[group] = result

        result['counts'].append({
            'date': date.date(),
            'new_patients': new_patients,
            'total_patients': total_patients,
        })

    return results

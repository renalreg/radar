from datetime import datetime

from sqlalchemy import cast, extract, Integer, func

from radar.lib.database import db


def recruitment_by_month(date_column, filters=None):
    year_column = cast(extract('year', date_column), Integer)
    month_column = cast(extract('month', date_column), Integer)

    query = db.session\
        .query(year_column, month_column, func.count())\
        .filter(date_column != None)\
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

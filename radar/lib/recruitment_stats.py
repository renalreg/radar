from datetime import datetime

import pandas
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

    data = [(datetime(year, month, 1), count) for year, month, count in query.all()]

    if not data:
        return []

    # Create a data frame
    df = pandas.DataFrame.from_records(data, columns=["date", "count"], index="date")

    # Create a month index
    df.index = df.index.to_period("M")

    # Fill in missing months
    df = df.reindex(pandas.period_range(df.index[0], df.index[-1], freq="M"), fill_value=0)

    # Cumulative sum
    df['total'] = df.cumsum()

    # Convert the data for the response
    df.index = df.index.to_datetime()
    data = [{'date': dt.date(), 'new': new, 'total': total} for dt, new, total in df.to_records()]

    return data

from datetime import datetime

import pandas
from sqlalchemy import cast, extract, Integer, func

from radar.lib.database import db


def recruitment_by_month(date_column, filters, cumulative=False):
    year_column = cast(extract('year', date_column), Integer)
    month_column = cast(extract('month', date_column), Integer)

    query = db.session\
        .query(year_column, month_column, func.count())\
        .filter(date_column != None)\
        .filter(*filters)\
        .group_by(year_column, month_column)\
        .order_by(year_column, month_column)

    data = [(datetime(year, month, 1), count) for year, month, count in query.all()]

    if not data:
        return list()

    # Create a data frame
    df = pandas.DataFrame.from_records(data, columns=["date", "count"], index="date")

    # Create a month index
    df.index = df.index.to_period("M")

    # Fill in missing months
    df = df.reindex(pandas.period_range(df.index[0], df.index[-1], freq="M"), fill_value=0)

    if cumulative:
        # Cumulative sum
        df = df.cumsum()

    # Convert the data for the response
    df.index = df.index.to_datetime()
    data = [(dt, int(value)) for dt, value in df.to_records()]

    return data
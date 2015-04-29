def datetime_format(dt, datetime_format):
    if dt is None:
        return ''
    else:
        return dt.strftime(datetime_format)
from datetime import date


def transform_values(data, f):
    """Apply a function (f) to the values in data."""

    if isinstance(data, list):
        r = [transform_values(v, f) for v in data]
    elif isinstance(data, dict):
        r = {k: transform_values(v, f) for k, v in data.items()}
    else:
        r = f(data)

    return r


def to_iso(value):
    if isinstance(value, date):
        value = date.isoformat()

    return value

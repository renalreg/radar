from radar.utils import get_attrs


def get_years(months):
    """Get whole number of years."""

    if months is None:
        years = 0
    else:
        years = months // 12

    return years


def get_months(months):
    """Get remaining months."""

    if months is None:
        months = 0
    else:
        months = months % 12

    return months


def path_getter(path):
    """Get attributes at the dot-separated path."""

    parts = path.split('.')

    def f(value):
        return get_attrs(value, *parts)

    return f


def none_getter(value):
    return None


def identity_getter(value):
    return value

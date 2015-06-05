from datetime import date, datetime


def required(value):
    if value is None:
        return 'This field is required.'


def not_empty(value):
    if value is None or len(value) == 0:
        return 'This field is required.'


def min_(min_value):
    def f(value):
        if value < min_value:
            return 'Must be greater than or equal to %s.' % min_value

    return f


def max_(max_value):
    def f(value):
        if value > max_value:
            return 'Must be less than or equal to %s.' % max_value

    return f


def range_(min_value=None, max_value=None):
    def f(value):
        if min_value is not None:
            r = min_(min_value)(value)

            if r is not None:
                return r

        if max_value is not None:
            r = max_(max_value)(value)

            if r is not None:
                return r

    return f


def in_(values):
    def f(value):
        if value not in values:
            return 'Not a valid value.'

    return f


def not_in_future(value):
    # Convert dates to datetimes
    if isinstance(value, date):
        value = datetime(value.year, value.month, value.day)

    if value > datetime.now():
        return "Can't be in the future."

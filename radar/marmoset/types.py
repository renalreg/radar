from datetime import datetime, date

import iso8601

from radar.marmoset.utils import identity


def parse_int(value):
    if isinstance(value, int):
        return value
    elif isinstance(value, basestring):
        try:
            return int(value)
        except ValueError:
            raise ValueError('Not an integer.')
    else:
        raise ValueError('Not an integer.')


def parse_float(value):
    if isinstance(value, float):
        return value
    elif isinstance(value, int):
        return float(value)
    elif isinstance(value, basestring):
        try:
            return float(value)
        except ValueError:
            raise ValueError('Not a float.')
    else:
        raise ValueError('Not a float.')


def parse_string(value):
    if isinstance(value, basestring):
        return value.strip()
    else:
        raise ValueError('Not a string.')


def parse_boolean(value):
    if isinstance(value, bool):
        return value
    else:
        raise ValueError('Not a boolean.')


def parse_date(value):
    if isinstance(value, date):
        return value
    elif isinstance(value, basestring):
        try:
            return iso8601.parse_date(value).date()
        except iso8601.ParseError:
            raise ValueError('Not a date.')
    else:
        raise ValueError('Not a date.')


def parse_datetime(value):
    if isinstance(value, datetime):
        return value
    elif isinstance(value, basestring):
        try:
            return iso8601.parse_date(value).date()
        except iso8601.ParseError:
            raise ValueError('Not a datetime.')
    else:
        raise ValueError('Not a datetime.')


format_string = identity
format_int = identity
format_float = identity
format_boolean = identity


def format_date(value):
    return value.isoformat()


def format_datetime(value):
    return value.isoformat()

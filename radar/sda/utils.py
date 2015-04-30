import collections
from datetime import datetime
import pytz
import dateutil.parser

ZONE = 'Europe/London'

def datetime_to_jsonb(dt):
    if dt.tzinfo is None:
        # Convert naive datetime to local timezone
        local = pytz.timezone(ZONE)
        dt = local.localize(dt)

    return dt.isoformat()

def jsonb_to_datetime(dt_str):
    dt = dateutil.parser.parse(dt_str)
    return dt

def serialize_jsonb(data):
    if isinstance(data, dict):
        new_data = dict()

        for key, value in data.items():
            new_data[key] = serialize_jsonb(value)

        return new_data
    elif isinstance(data, list):
        new_data = list()

        for value in data:
            new_data.append(serialize_jsonb(value))

        return new_data
    elif isinstance(data, datetime):
        return datetime_to_jsonb(data)
    else:
        return data
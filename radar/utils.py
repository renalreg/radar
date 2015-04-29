from datetime import datetime

from flask import request, url_for


def get_path(data, *keys):
    for key in keys:
        data = data.get(key)

        if data is None:
            return None

    return data


def get_path_as_datetime(data, *keys):
    value = get_path(data, *keys)

    if value is not None:
        value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')

    return value
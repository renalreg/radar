import dateutil.parser
from flask import request


def get_path(data, keys):
    for key in keys:
        data = data.get(key)

        if data is None:
            return None

    return data


def get_path_as_text(data, keys):
    value = get_path(data, keys)

    if value is not None:
        value = str(value)

    return value


def get_path_as_datetime(data, keys):
    value = get_path_as_text(data, keys)

    if value is not None:
        value = dateutil.parser.parse(value)

    return value


def optional_int(value):
    if not value:
        return None

    return int(value)


def set_path(data, keys, value):
    for key in keys[:-1]:
        if key not in data:
            data[key] = {}

        data = data[key]

    data[keys[-1]] = value


def get_request_args():
    args = request.args.to_dict(flat=False)
    args.update(request.view_args)
    return args
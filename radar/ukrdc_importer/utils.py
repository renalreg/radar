import uuid
import calendar
from datetime import datetime

from cornflake.exceptions import ValidationError

from radar.database import db
from radar.models.groups import Group, GROUP_TYPE, GROUP_CODE_UKRDC
from radar.models.users import User


NAMESPACE = uuid.UUID('91bce7f1-ea5f-4c98-8350-33d65d597a10')
USERNAME = 'ukrdc_importer'


def validate_list(items, serializer, invalid_f=None):
    valid_items = list()

    for i, item in enumerate(items):
        try:
            validated_data = serializer.run_validation(item)
        except ValidationError as e:
            if invalid_f is not None:
                invalid_f(i, item, e)
        else:
            valid_items.append(validated_data)

    return valid_items


def unique_list(items, key_f, duplicate_f):
    unique_items = list()
    seen = set()

    for i, item in enumerate(items):
        if key_f is None:
            key = item
        else:
            key = key_f(item)

        if key not in seen:
            unique_items.append(item)
            seen.add(key)
        elif duplicate_f is not None:
            duplicate_f(item)

    return unique_items


def delete_list(items, items_to_keep, delete_f=None):
    items_to_delete = set(items) - set(items_to_keep)

    for item in items_to_delete:
        if delete_f is not None:
            delete_f(item)

        db.session.delete(item)

    return items_to_delete


def build_id(*names):
    x = NAMESPACE

    for name in names:
        x = uuid.uuid5(x, str(name))

    return str(x)


def get_path(data, *path):
    value = data

    for key in path:
        value = value.get(key)

        if value is None:
            break

    return value


def update_path(data, f, *path):
    rest, last = path[:-1], path[-1]

    data = get_path(data, *rest)

    if data is None:
        return

    value = data.get(last)

    if value is None:
        return

    data[last] = f(value)


def get_import_group():
    return Group.query.filter(Group.type == GROUP_TYPE.OTHER, Group.code == GROUP_CODE_UKRDC).one()


def get_import_user():
    return User.query.filter(User.username == USERNAME).one()


def get_group(code):
    return Group.query.filter(Group.code == code).first()


def utc():
    return calendar.timegm(datetime.utcnow().utctimetuple())

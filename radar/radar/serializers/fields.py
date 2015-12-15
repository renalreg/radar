from datetime import datetime, date
import six
from uuid import UUID

import delorean

from radar.serializers.core import Field
from radar.validation.core import ValidationError


class StringField(Field):
    default_error_messages = {
        'invalid': 'A valid string is required.'
    }

    def __init__(self, **kwargs):
        self.trim_whitespace = kwargs.pop('trim_whitespace', True)
        super(StringField, self).__init__(**kwargs)

    def to_value(self, data):
        if data is None:
            return None

        if isinstance(data, dict) or isinstance(data, list) or isinstance(data, bool):
            self.fail('invalid')

        value = six.text_type(data)

        if self.trim_whitespace:
            value = value.strip()

        return value

    def to_data(self, value):
        if value is None:
            return None

        data = six.text_type(value)

        return data


class BooleanField(Field):
    default_error_messages = {
        'invalid': 'A valid boolean is required.'
    }

    TRUE_VALUES = {'t', 'true', 'y', 'yes', '1', 1, True}
    FALSE_VALUES = {'f', 'false', 'n', 'no', '0', 0, False}

    def to_value(self, data):
        if data is None:
            return None

        if hasattr(data, 'lower'):
            data = data.lower()

        # Check for TypeError as list and dict aren't hashable
        try:
            if data in self.TRUE_VALUES:
                return True
            elif data in self.FALSE_VALUES:
                return False
            else:
                self.fail('invalid')
        except TypeError:
            self.fail('invalid')

    def to_data(self, value):
        if value is None:
            return None

        return bool(value)


class IntegerField(Field):
    default_error_messages = {
        'invalid': 'A valid integer is required.'
    }

    def to_value(self, data):
        if data is None:
            return None

        if isinstance(data, basestring):
            data = data.strip()

            if len(data) == 0:
                return None

        try:
            value = int(data)
            value_f = float(data)

            # No floats
            if value != value_f:
                self.fail('invalid')
        except (ValueError, TypeError):
            self.fail('invalid')

        return value

    def to_data(self, value):
        if value is None:
            return None

        return int(value)


class FloatField(Field):
    default_error_messages = {
        'invalid': 'A valid number is required.'
    }

    def to_value(self, data):
        if data is None:
            return None

        if isinstance(data, basestring):
            data = data.strip()

            if len(data) == 0:
                return None

        try:
            value = float(data)
        except (ValueError, TypeError):
            self.fail('invalid')

        return value

    def to_data(self, value):
        if value is None:
            return None

        return float(value)


class DateField(Field):
    default_error_messages = {
        'invalid': 'Date has wrong format.',
        'datetime': 'Expected a date but got a datetime.',
    }

    def to_value(self, data):
        if data is None:
            return None
        elif isinstance(data, datetime):
            self.fail('datetime')
        elif isinstance(data, date):
            # Already a date
            return data
        elif not isinstance(data, six.string_types):
            # Not a string
            self.fail('invalid')
        else:
            try:
                value = delorean.parse(data).date
            except ValueError:
                self.fail('invalid')

            return value

    def to_data(self, value):
        if value is None:
            return None

        # TODO always %Y-%m-%d
        return value.isoformat()


class DateTimeField(Field):
    default_error_messages = {
        'invalid': 'Datetime has wrong format.',
        'date': 'Expected a date but got a datetime.',
    }

    def to_value(self, data):
        if data is None:
            return None
        elif isinstance(data, datetime):
            # Already a datetime
            return data
        elif isinstance(data, date):
            self.fail('date')
        elif not isinstance(data, six.string_types):
            # Not a string
            self.fail('invalid')
        else:
            try:
                value = delorean.parse(data).datetime
            except ValueError:
                self.fail('invalid')

            return value

    def to_data(self, value):
        # TODO always %Y-%m-%dT%H:%M:%S+00:00
        return value.isoformat()


class ListField(Field):
    default_error_messages = {
        'not_a_list': 'Expected a list.'
    }

    def __init__(self, field, **kwargs):
        super(ListField, self).__init__(**kwargs)
        self.field = field

    def to_value(self, data):
        if data is None:
            return None

        if not isinstance(data, list):
            self.fail('not_a_list')

        values = []
        errors = {}

        for i, x in enumerate(data):
            try:
                value = self.field.to_value(x)
            except ValidationError as e:
                errors[i] = e.errors
            else:
                values.append(value)

        if errors:
            raise ValidationError(errors)

        return values

    def to_data(self, values):
        if values is None:
            return None

        data = []

        for value in values:
            if value is None:
                data.append(None)
            else:
                data.append(self.field.to_data(value))

        return data

    def transform_errors(self, errors):
        transformed_errors = {}

        # Errors on the list field
        if '_' in errors:
            transformed_errors['_'] = errors['_']

        for i, field_errors in errors.items():
            if isinstance(i, int):
                transformed_field_errors = self.field.transform_errors(field_errors)
                transformed_errors[i] = transformed_field_errors

        return transformed_errors


class CommaSeparatedStringField(Field):
    def to_value(self, data):
        if data is None:
            return None

        return [x.strip() for x in data.split(',')]

    def to_data(self, value):
        return ','.join(value)


class UUIDField(Field):
    default_error_messages = {
        'invalid': 'A valid UUID is required.'
    }

    def __init__(self, **kwargs):
        super(UUIDField, self).__init__(**kwargs)

    def to_value(self, data):
        if data is None:
            return None

        if isinstance(data, dict) or isinstance(data, list) or isinstance(data, bool):
            self.fail('invalid')

        value = six.text_type(data)

        try:
            UUID(data)
        except ValueError:
            self.fail('invalid')

        return value

    def to_data(self, value):
        if value is None:
            return None

        data = six.text_type(value)

        return data


class EnumField(Field):
    default_error_messages = {
        'invalid': 'Not a valid value.'
    }

    def __init__(self, enum, **kwargs):
        super(EnumField, self).__init__(self, **kwargs)
        self.enum = enum

    def to_value(self, data):
        if data is None:
            return None

        try:
            value = self.enum(data)
        except ValueError:
            self.fail('invalid')

        return value

    def to_data(self, value):
        if value is None:
            return None

        data = six.text_type(value)

        return data

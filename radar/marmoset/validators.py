from datetime import date, datetime

from cornflake.exceptions import ValidationError
import pytz


class Validator(object):
    def __init__(self, field, validator_data):
        pass

    @classmethod
    def get_schema(cls):
        raise NotImplementedError()

    def __call__(self, value):
        raise NotImplementedError()


class InValidator(Validator):
    def __init__(self, field, validator_data):
        self.values = []

        for value in validator_data['values']:
            if value is not None:
                value = field.parser(value)

            if isinstance(value, list):
                self.values.extend(value)
            else:
                self.values.append(value)

    @classmethod
    def get_schema(cls):
        return {
            'type': 'object',
            'properties': {
                'name': {
                    'enum': ['in']
                },
                'values': {
                    'type': 'array'
                }
            },
            'required': ['name', 'values'],
            'additionalProperties': False
        }

    def __call__(self, value):
        try:
            if isinstance(value, basestring):
                raise TypeError
            if not set(value).issubset(self.values):
                raise ValidationError('Not a valid value.')
        except TypeError:
            if value not in self.values:
                raise ValidationError('Not a valid value.')


class MinValidator(Validator):
    def __init__(self, field, validator_data):
        self.value = field.parser(validator_data['value'])

    @classmethod
    def get_schema(cls):
        return {
            'type': 'object',
            'properties': {
                'name': {
                    'enum': ['min']
                },
                'value': {}
            },
            'required': ['name', 'value'],
            'additionalProperties': False
        }

    def __call__(self, value):
        if value < self.value:
            raise ValidationError('Must be greater than or equal to {0}.'.format(self.value))


class MaxValidator(Validator):
    def __init__(self, field, validator_data):
        self.value = field.parser(validator_data['value'])

    @classmethod
    def get_schema(cls):
        return {
            'type': 'object',
            'properties': {
                'name': {
                    'enum': ['max']
                },
                'value': {}
            },
            'required': ['name', 'value'],
            'additionalProperties': False
        }

    def __call__(self, value):
        if value > self.value:
            raise ValidationError('Must be less than or equal to {0}.'.format(self.value))


class NotInFutureValidator(Validator):
    @classmethod
    def get_schema(cls):
        return {
            'type': 'object',
            'properties': {
                'name': {
                    'enum': ['notInFuture']
                }
            },
            'required': ['name'],
            'additionalProperties': False
        }

    def __call__(self, value):
        if isinstance(value, datetime):
            now = datetime.now(tz=pytz.UTC)
        else:
            now = date.today()

        if value > now:
            raise ValidationError("Can't be in the future.")

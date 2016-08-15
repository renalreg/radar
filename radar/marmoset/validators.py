from datetime import date

from cornflake.exceptions import ValidationError


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

            self.values.append(value)

    @classmethod
    def get_schema(cls):
        return {
            'type': 'object',
            'properties': {
                'type': {
                    'enum': ['in']
                },
                'values': {
                    'type': 'array'
                }
            },
            'required': ['type', 'values'],
            'additionalProperties': False
        }

    def __call__(self, value):
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
                'type': {
                    'enum': ['min']
                },
                'value': {}
            },
            'required': ['type', 'value'],
            'additionalProperties': False
        }

    def __call__(self, value):
        if value < self.value:
            raise ValidationError('Must be greater than or equal to {0}.'.format(value))


class MaxValidator(Validator):
    def __init__(self, field, validator_data):
        self.value = field.parser(validator_data['value'])

    @classmethod
    def get_schema(cls):
        return {
            'type': 'object',
            'properties': {
                'type': {
                    'enum': ['max']
                },
                'value': {}
            },
            'required': ['type', 'value'],
            'additionalProperties': False
        }

    def __call__(self, value):
        if value > self.value:
            raise ValidationError('Must be less than or equal to {0}.'.format(value))


class NotInFutureValidator(Validator):
    @classmethod
    def get_schema(cls):
        return {
            'type': 'object',
            'properties': {
                'type': {
                    'enum': ['notInFuture']
                }
            },
            'required': ['type'],
            'additionalProperties': False
        }

    def __call__(self, value):
        if value > date.today():
            raise ValidationError("Can't be in the future.")

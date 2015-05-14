class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


class StopValidation(Exception):
    pass


def required(value):
    if value is None:
        raise ValidationError('This field is required.')


def not_empty(value):
    if value is None or len(value) == 0:
        raise ValidationError('This field is required.')


def optional(value):
    if value is None:
        raise StopValidation()
from collections import defaultdict
from datetime import datetime
from radar.utils import humanize_datetime_format


class FormHandler(object):
    parsers = {}

    def __init__(self, obj=None):
        self.obj = obj
        self.form_data = {}
        self._reset()

    def _parse(self):
        for model_key, parser in self.parsers.items():
            try:
                model_value = parser(self.form_data, self.stash, model_key)
            except ParseError as e:
                self.errors[model_key].append(e.message)
                model_value = None

            self.set_model_value(model_key, model_value)

    def _reset(self):
        self.errors = defaultdict(list)
        self.stash = {}

    def set_model_value(self, model_key, model_value):
        if self.obj is None:
            return

        if isinstance(self.obj, dict):
            self.obj[model_key] = model_value
        else:
            setattr(self.obj, model_key, model_value)

    def get_model_value(self, model_key):
        if self.obj is None:
            return None

        if isinstance(self.obj, dict):
            return self.obj.get(model_key)
        else:
            return getattr(self.obj, model_key)

    def add_errors(self, errors):
        for model_key, model_errors in errors.items():
            # There weren't parse errors
            if len(self.errors[model_key]) == 0:
                self.errors[model_key] = model_errors

    def validate(self):
        pass

    def valid(self):
        return not any(len(x) for x in self.errors)

    def submit(self, form_data):
        self.form_data = form_data

        self._reset()
        self._parse()
        self.validate()

class ParseError(Exception):
    def __init__(self, message):
        self.message = message

def str_parser(form_data, stash, model_key):
    model_value = form_data.get(model_key)

    if model_value is not None:
        model_value = model_value.strip()

    return model_value

def date_parser(date_format='%d/%m/%Y'):
    return datetime_parser(date_format)

def datetime_parser(datetime_format='%d/%m/%Y %H:%M:%S'):
    def f(form_data, stash, model_key):
        model_value = str_parser(form_data, stash, model_key)

        if model_value:
            try:
                return datetime.strptime(model_value, datetime_format)
            except ValueError:
                # TODO check format and validity separately
                stash[model_key] = model_value
                raise ParseError('Date must be in "%s" format.' % humanize_datetime_format(datetime_format))
        else:
            return None

    return f

def int_parser(form_data, stash, model_key):
    model_value = str_parser(form_data, stash, model_key)

    if model_value:
        try:
            return int(model_value)
        except ValueError:
            stash[model_key] = model_value
            raise ParseError('Not an integer.')
    else:
        return None

def positive_int_parser(form_data, stash, model_key):
    model_value = int_parser(form_data, stash, model_key)

    if model_value is not None and model_value < 0:
        raise ParseError('Not a positive integer.')

    return model_value
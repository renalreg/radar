from collections import defaultdict
from datetime import datetime


class FormHandler(object):
    parsers = {}

    def __init__(self, obj):
        self.obj = obj
        self.form_data = {}
        self._reset()

    def _parse(self):
        for model_attr, parser in self.parsers.items():
            try:
                model_value = parser(self.form_data, self.stash, model_attr)
            except ParseError as e:
                self.errors[model_attr].append(e.message)
                model_value = None

            setattr(self.obj, model_attr, model_value)

    def _reset(self):
        self.errors = defaultdict(list)
        self.stash = {}

    def add_errors(self, errors):
        for model_attr, model_errors in errors.items():
            # There weren't parse errors
            if len(self.errors[model_attr]) == 0:
                self.errors[model_attr] = model_errors

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

def str_parser(form_data, stash, model_attr):
    model_value = form_data.get(model_attr)

    if model_value is not None:
        model_value = model_value.strip()

    return model_value

def datetime_parser(datetime_format):
    def f(form_data, stash, model_attr):
        model_value = str_parser(form_data, stash, model_attr)

        if model_value:
            try:
                return datetime.strptime(model_value, datetime_format)
            except ValueError:
                # TODO check format and validity separately
                stash[model_attr] = model_value
                raise ParseError('Date must be in "%s" format.' % humanize_datetime_format(datetime_format))
        else:
            return None

    return f

def int_parser(form_data, stash, model_attr):
    model_value = str_parser(form_data, stash, model_attr)

    if model_value:
        try:
            return int(model_value)
        except ValueError:
            stash[model_attr] = model_value
            raise ParseError('Not an integer.')
    else:
        return None

# TODO complete
def humanize_datetime_format(datetime_format):
    output = datetime_format.replace('%d', 'DD')
    output = output.replace('%m', 'MM')
    output = output.replace('%Y', 'YYYY')
    return output
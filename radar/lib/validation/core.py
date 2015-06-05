from datetime import date, datetime


class BaseErrorHandler(object):
    def __init__(self):
        self.valid = True

    def is_valid(self):
        return self.valid


class ErrorHandler(BaseErrorHandler):
    def __init__(self):
        super(ErrorHandler, self).__init__()

        self.errors = dict()

    def add_error(self, field_path, error):
        if isinstance(field_path, basestring):
            field_path = (field_path, )

        self.valid = False

        if field_path not in self.errors:
            self.errors[field_path] = [error]
        else:
            self.errors[field_path].append(error)


class ProxyErrorHandler(BaseErrorHandler):
    def __init__(self, errors, prefix):
        super(ProxyErrorHandler, self).__init__()

        self.errors = errors
        self.prefix = prefix

    def add_error(self, field_path, error):
        if isinstance(field_path, basestring):
            field_path = (field_path, )

        self.valid = False

        field_path = self.prefix + field_path

        self.errors.add_error(field_path, error)


class FormErrorHandler(BaseErrorHandler):
    def __init__(self, form):
        super(FormErrorHandler, self).__init__()

        self.form = form

    def add_error(self, field_path, error):
        if isinstance(field_path, basestring):
            field_path = (field_path, )

        self.valid = False

        # TODO
        if len(field_path) > 1:
            raise NotImplementedError

        field_name = field_path[0]

        form_field = getattr(self.form, field_name, None)

        if form_field is None:
            form_field = getattr(self.form, field_name + '_id', None)

        if form_field is not None:
            form_field.errors.append(error)


def run_validators(errors, field_name, value, validators):
    for validator in validators:
        error = validator(value)

        if error:
            errors.add_error(field_name, error)
            break

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


def required(value):
    if value is None:
        return 'This field is required.'


def not_empty(value):
    if value is None or len(value) == 0:
        return 'This field is required.'


def min_(min_value):
    def f(value):
        if value < min_value:
            return 'Must be greater than or equal to %s.' % min_value

    return f


def max_(max_value):
    def f(value):
        if value > max_value:
            return 'Must be less than or equal to %s.' % max_value

    return f


def range_(min_value=None, max_value=None):
    def f(value):
        if min_value is not None:
            r = min_(min_value)(value)

            if r is not None:
                return r

        if max_value is not None:
            r = max_(max_value)(value)

            if r is not None:
                return r

    return f


def in_(values):
    def f(value):
        if value not in values:
            return 'Not a valid value.'

    return f


def run_validators(errors, field_name, value, validators):
    for validator in validators:
        error = validator(value)

        if error:
            errors.add_error(field_name, error)
            break

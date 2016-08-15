import pkg_resources

from radar.marmoset.base_registry import BaseRegistry
from radar.marmoset.handlers import (
    JSDefaultHandler,
    JSRequiredHandler,
    JSVisibleHandler,
)
from radar.marmoset.types import (
    format_boolean,
    format_date,
    format_datetime,
    format_float,
    format_int,
    format_string,
    parse_boolean,
    parse_date,
    parse_datetime,
    parse_float,
    parse_int,
    parse_string,
)
from radar.marmoset.validators import (
    InValidator,
    MaxValidator,
    MinValidator,
    NotInFutureValidator,
)

HELPERS = pkg_resources.resource_string(__name__, 'helpers.js')


class Registry(BaseRegistry):
    def __init__(self):
        super(Registry, self).__init__()

        # Add parsers
        self.add_parser('string', parse_string)
        self.add_parser('int', parse_int)
        self.add_parser('float', parse_float)
        self.add_parser('boolean', parse_boolean)
        self.add_parser('date', parse_date)
        self.add_parser('datetime', parse_datetime)

        # Add formatters
        self.add_formatter('string', format_string)
        self.add_formatter('int', format_int)
        self.add_formatter('float', format_float)
        self.add_formatter('boolean', format_boolean)
        self.add_formatter('date', format_date)
        self.add_formatter('datetime', format_datetime)

        # Add default handlers
        self.add_default('foo', 'js', JSDefaultHandler)  # TODO

        # Add required handlers
        self.add_required('js', JSRequiredHandler)

        # Add visible handlers
        self.add_visible('js', JSVisibleHandler)

        # Add validators
        self.add_validator('int', 'in', InValidator)
        self.add_validator('int', 'min', MinValidator)
        self.add_validator('int', 'max', MaxValidator)
        self.add_validator('date', 'notInFuture', NotInFutureValidator)

        # Add helpers
        self.add_js(HELPERS)

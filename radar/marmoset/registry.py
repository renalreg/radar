import pkg_resources

from radar.marmoset.base_registry import BaseRegistry
from radar.marmoset.handlers import (
    JSDefaultHandler,
    JSFormulaHandler,
    JSRequiredHandler,
    JSVisibleHandler,
)
from radar.marmoset.types import (
    format_boolean,
    format_date,
    format_datetime,
    format_float,
    format_int,
    format_list,
    format_string,
    parse_boolean,
    parse_date,
    parse_datetime,
    parse_float,
    parse_int,
    parse_list,
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

        # Add types
        self.add_type('string', parse_string, format_string)
        self.add_type('int', parse_int, format_int)
        self.add_type('float', parse_float, format_float)
        self.add_type('boolean', parse_boolean, format_boolean)
        self.add_type('date', parse_date, format_date)
        self.add_type('datetime', parse_datetime, format_datetime)
        self.add_type('array', parse_list, format_list)
        self.add_type('text', parse_string, format_string)

        # Add default handlers
        self.add_default('js', JSDefaultHandler)

        # Add required handlers
        self.add_required('js', JSRequiredHandler)

        # Add visible handlers
        self.add_visible('js', JSVisibleHandler)

        # Add validators
        self.add_validator('in', InValidator)
        self.add_validator('min', MinValidator)
        self.add_validator('max', MaxValidator)
        self.add_validator('notInFuture', NotInFutureValidator, type='date')
        self.add_validator('notInFuture', NotInFutureValidator, type='datetime')

        # Add formula handlers
        self.add_formula('js', JSFormulaHandler)

        # Add helpers
        self.add_js(HELPERS)

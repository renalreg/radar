from radar.lib.validation.core import run_validators
from radar.lib.validation.validators import required, not_in_future


def validate_hospitalisation(errors, obj):
    run_validators(errors, 'date_of_admission', obj.date_of_admission, [required, not_in_future])

    if not errors.is_valid():
        return

    if obj.date_of_discharge is not None:
        run_validators(errors, 'date_of_discharge', obj.date_of_discharge, [not_in_future])

        if obj.date_of_admission > obj.date_of_discharge:
            errors.add_error('date_of_discharge', 'Date of discharge must be on or after date of admission.')

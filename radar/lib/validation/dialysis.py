from radar.lib.validation.core import run_validators
from radar.lib.validation.validators import required, not_in_future


def validate_dialysis(errors, obj):
    run_validators(errors, 'from_date', obj.from_date, [required, not_in_future])
    run_validators(errors, 'dialysis_type', obj.dialysis_type, [required])

    if not errors.is_valid():
        return

    if obj.to_date is not None:
        run_validators(errors, 'to_date', obj.to_date, [not_in_future])

        if obj.from_date > obj.to_date:
            errors.add_error('to_date', 'Must be after from date.')

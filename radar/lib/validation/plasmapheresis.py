from radar.lib.validation.core import run_validators
from radar.lib.validation.validators import required


def validate_plasmapheresis(errors, obj):
    run_validators(errors, 'from_date', obj.from_date, [required])
    run_validators(errors, 'no_of_exchanges', obj.no_of_exchanges, [required])
    run_validators(errors, 'response', obj.response, [required])

    if not errors.is_valid():
        return

    if obj.to_date is not None:
        if obj.from_date > obj.to_date:
            errors.add_error('to_date', 'Must be after from date.')

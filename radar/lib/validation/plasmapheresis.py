from radar.lib.validation.core import run_validators
from radar.lib.validation.patient_validators import after_date_of_birth
from radar.lib.validation.validators import required, not_in_future, optional, min_


def validate_plasmapheresis(errors, obj):
    patient = obj.patient

    run_validators(errors, 'from_date', obj.from_date, [required, after_date_of_birth(patient), not_in_future])
    run_validators(errors, 'to_date', obj.to_date, [optional, after_date_of_birth(patient), not_in_future])
    run_validators(errors, 'no_of_exchanges', obj.no_of_exchanges, [required, min_(0)])
    run_validators(errors, 'response', obj.response, [required])

    if not errors.is_valid():
        return

    if obj.to_date is not None and obj.from_date > obj.to_date:
        errors.add_error('to_date', 'Must be after from date.')

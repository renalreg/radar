from radar.lib.validation.core import run_validators
from radar.lib.validation.patient_validators import after_date_of_birth
from radar.lib.validation.validators import required, not_empty, not_in_future, min_, optional


def validate_medication(errors, obj):
    patient = obj.patient

    run_validators(errors, 'from_date', obj.from_date, [required, after_date_of_birth(patient), not_in_future])
    run_validators(errors, 'to_date', obj.to_date, [optional, after_date_of_birth(patient), not_in_future])
    run_validators(errors, 'name', obj.name, [not_empty])
    run_validators(errors, 'dose_quantity', obj.dose_quantity, [required, min_(0)])
    run_validators(errors, 'dose_unit', obj.dose_unit, [required])
    run_validators(errors, 'frequency', obj.frequency, [required])
    run_validators(errors, 'route', obj.route, [required])

    if not errors.is_valid():
        return

    if obj.to_date is not None:
        run_validators(errors, 'to_date', obj.to_date, [not_in_future])

        if obj.from_date > obj.to_date:
            errors.add_error('to_date', 'Must be after from date.')

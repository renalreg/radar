from radar.lib.validation.core import run_validators, required, not_empty


def validate_medication(errors, obj):
    run_validators(errors, 'from_date', obj.from_date, [required])
    run_validators(errors, 'name', obj.name, [not_empty])
    run_validators(errors, 'dose_quantity', obj.dose_quantity, [required])
    run_validators(errors, 'dose_unit', obj.dose_unit, [required])
    run_validators(errors, 'frequency', obj.frequency, [required])
    run_validators(errors, 'route', obj.route, [required])

    if not errors.is_valid():
        return

    if obj.to_date is not None:
        if obj.from_date > obj.to_date:
            errors.add_error('to_date', 'Must be after from date.')

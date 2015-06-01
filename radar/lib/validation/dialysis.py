from radar.lib.validation.core import run_validators, required


def validate_dialysis(errors, obj):
    run_validators(errors, 'from_date', obj.from_date, [required])
    run_validators(errors, 'dialysis_type', obj.dialysis_type, [required])

    if not errors.is_valid():
        return

    if obj.to_date is not None:
        if obj.from_date > obj.to_date:
            errors.add_error('to_date', 'Must be after from date.')
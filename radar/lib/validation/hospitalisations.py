from radar.lib.validation.core import run_validators, required


def validate_hospitalisation(errors, obj):
    run_validators(errors, 'date_of_admission', obj.date_of_admission, [required])

    if not errors.is_valid():
        return

    if obj.date_of_discharge is not None:
        if obj.date_of_admission > obj.date_of_discharge:
            errors.add_error('to_date', 'Date of discharge must be on or after date of admission.')
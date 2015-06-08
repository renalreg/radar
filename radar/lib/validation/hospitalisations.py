from radar.lib.validation.core import run_validators
from radar.lib.validation.patient_validators import after_date_of_birth
from radar.lib.validation.validators import required, not_in_future, optional


def validate_hospitalisation(errors, obj):
    patient = obj.patient

    run_validators(errors, 'date_of_admission', obj.date_of_admission, [required, after_date_of_birth(patient), not_in_future])
    run_validators(errors, 'date_of_discharge', obj.date_of_discharge, [optional, after_date_of_birth(patient), not_in_future])

    if not errors.is_valid():
        return

    if obj.date_of_discharge is not None and obj.date_of_admission > obj.date_of_discharge:
        errors.add_error('date_of_discharge', 'Date of discharge must be on or after date of admission.')

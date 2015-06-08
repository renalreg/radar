from radar.lib.validation.core import run_validators
from radar.lib.validation.patient_validators import after_date_of_birth
from radar.lib.validation.validators import required, not_in_future


def validate_transplant(errors, obj):
    patient = obj.patient

    run_validators(errors, 'transplant_date', obj.transplant_date, [required, after_date_of_birth(patient), not_in_future])
    run_validators(errors, 'transplant_type', obj.transplant_type, [required])

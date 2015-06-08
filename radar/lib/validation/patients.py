from radar.lib.validation.core import run_validators
from radar.lib.validation.validators import required, not_empty, not_in_future, optional, in_


def validate_patient_demographics(errors, obj):
    run_validators(errors, 'first_name', obj.first_name, [not_empty])
    run_validators(errors, 'last_name', obj.first_name, [not_empty])
    run_validators(errors, 'date_of_birth', obj.date_of_birth, [required])
    run_validators(errors, 'date_of_death', obj.date_of_death, [optional, not_in_future])
    run_validators(errors, 'gender', obj.gender, [required, in_(['M', 'F'])])
    run_validators(errors, 'ethnicity_code', obj.ethnicity_code, [required])

    if not errors.is_valid():
        return

    if obj.date_of_death is not None and obj.date_of_death < obj.date_of_birth:
        errors.add_error('date_of_death', "Can't be before the patient's date of birth.")

from radar.lib.validation.core import run_validators
from radar.lib.validation.validators import required, not_empty, not_in_future, optional, in_, email_address, nhs_no, \
    chi_no, max_length


def validate_patient_demographics(errors, obj):
    run_validators(errors, 'first_name', obj.first_name, [not_empty, max_length(30)])
    run_validators(errors, 'last_name', obj.last_name, [not_empty, max_length(30)])
    run_validators(errors, 'date_of_birth', obj.date_of_birth, [required, not_in_future])
    run_validators(errors, 'date_of_death', obj.date_of_death, [optional, not_in_future])
    run_validators(errors, 'gender', obj.gender, [required, in_(['M', 'F'])])
    run_validators(errors, 'ethnicity_code', obj.ethnicity_code, [required])
    run_validators(errors, 'email_address', obj.email_address, [optional, email_address])
    run_validators(errors, 'nhs_no', obj.nhs_no, [optional, nhs_no])
    run_validators(errors, 'chi_no', obj.chi_no, [optional, chi_no])

    if not errors.is_valid():
        return

    if obj.date_of_death is not None and obj.date_of_death < obj.date_of_birth:
        errors.add_error('date_of_death', "Can't be before the patient's date of birth.")

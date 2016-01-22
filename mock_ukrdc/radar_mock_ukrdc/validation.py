from radar.validation.core import Validation, Field
from radar.validation.validators import required


class OrganizationValidation(Validation):
    code = Field([required()])


class PatientNameValidation(Validation):
    given_name = Field([required()])
    family_name = Field([required()])


class PatientNumberValidation(Validation):
    number = Field([required()])
    organization = OrganizationValidation([required()])


class PatientSearchValidation(Validation):
    name = PatientNameValidation([required()])
    birth_time = Field([required()])
    patient_number = PatientNumberValidation([required()])

from radar.validation.core import Validation, Field
from radar.validation.validators import required


class PatientNameValidation(Validation):
    given = Field([required()])
    family = Field([required()])


class PatientNumberValidation(Validation):
    number = Field([required()])
    code_system = Field([required()])


class PatientSearchValidation(Validation):
    name = PatientNameValidation([required()])
    birth_time = Field([required()])
    patient_number = PatientNumberValidation([required()])

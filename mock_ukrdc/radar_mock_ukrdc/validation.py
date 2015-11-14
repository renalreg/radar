from radar.validation.core import Validation, Field
from radar.validation.validators import required


class PatientSearchValidation(Validation):
    first_name = Field([required()])
    last_name = Field([required()])
    date_of_birth = Field([required()])

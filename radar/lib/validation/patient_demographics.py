from radar.lib.validation.core import Validation, Field
from radar.lib.validation.data_sources import DataSourceValidationMixin
from radar.lib.validation.patients import PatientValidationMixin
from radar.lib.validation.validators import required, not_empty, optional, not_in_future, max_length, in_

class PatientDemographicsValidation(PatientValidationMixin, DataSourceValidationMixin, Validation):
    first_name = Field(chain=[not_empty(), max_length(30)])
    last_name = Field(chain=[not_empty(), max_length(30)])
    date_of_birth = Field(chain=[required(), not_in_future()])
    date_of_death = Field(chain=[optional(), not_in_future()])
    gender = Field(chain=[required(), in_(['M', 'F'])])
    ethnicity_code = Field(chain=[required()])

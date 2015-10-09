from radar.validation.core import Validation, Field, pass_new_obj, ValidationError
from radar.validation.data_sources import DataSourceValidationMixin
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, optional, valid_date_for_patient, max_length, none_if_blank


class HospitalisationValidation(PatientValidationMixin, DataSourceValidationMixin, MetaValidationMixin, Validation):
    date_of_admission = Field([required(), valid_date_for_patient()])
    date_of_discharge = Field([optional(), valid_date_for_patient()])
    reason_for_admission = Field([none_if_blank(), optional(), max_length(1000)])
    comments = Field([none_if_blank(), optional(), max_length(10000)])

    @pass_new_obj
    def validate_date_of_discharge(self, obj, date_of_discharge):
        if date_of_discharge < obj.date_of_admission:
            raise ValidationError('Must be on or before date of admission.')

        return date_of_discharge

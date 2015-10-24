from radar.models.nephrectomies import NEPHRECTOMY_KIDNEY_SIDES, NEPHRECTOMY_KIDNEY_TYPES, NEPHRECTOMY_KIDNEY_TYPES
from radar.validation.core import Field, Validation, ValidationError, pass_new_obj
from radar.validation.data_sources import DataSourceValidationMixin
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import valid_date_for_patient, required, in_


class NephrectomyValidation(PatientValidationMixin, DataSourceValidationMixin, MetaValidationMixin, Validation):
    date = Field([required(), valid_date_for_patient()])
    kidney_side = Field([required(), in_(NEPHRECTOMY_KIDNEY_SIDES.keys())])
    kidney_type = Field([required(), in_(NEPHRECTOMY_KIDNEY_TYPES.keys())])
    entry_type = Field([required(), in_(NEPHRECTOMY_KIDNEY_TYPES.keys())])

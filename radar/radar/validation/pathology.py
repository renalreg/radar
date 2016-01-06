from radar.models import PATHOLOGY_KIDNEY_TYPES, PATHOLOGY_KIDNEY_SIDES
from radar.validation.core import Validation, Field
from radar.validation.data_sources import DataSourceValidationMixin
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import valid_date_for_patient, required, in_, \
    max_length, none_if_blank, optional


class PathologyValidation(PatientValidationMixin, DataSourceValidationMixin, MetaValidationMixin, Validation):
    date = Field([required(), valid_date_for_patient()])
    kidney_type = Field([required(), in_(PATHOLOGY_KIDNEY_TYPES.keys())])
    kidney_side = Field([required(), in_(PATHOLOGY_KIDNEY_SIDES.keys())])
    reference_number = Field([none_if_blank(), optional(), max_length(100)])
    histological_summary = Field([none_if_blank(), optional(), max_length(1000)])

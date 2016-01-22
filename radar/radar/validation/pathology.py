from radar.models import PATHOLOGY_KIDNEY_TYPES, PATHOLOGY_KIDNEY_SIDES
from radar.validation.core import Validation, Field
from radar.validation.sources import RadarSourceValidationMixin
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import valid_date_for_patient, required, in_, \
    max_length, none_if_blank, optional, url


class PathologyValidation(PatientValidationMixin, RadarSourceValidationMixin, MetaValidationMixin, Validation):
    date = Field([required(), valid_date_for_patient()])
    kidney_type = Field([optional(), in_(PATHOLOGY_KIDNEY_TYPES.keys())])
    kidney_side = Field([optional(), in_(PATHOLOGY_KIDNEY_SIDES.keys())])
    reference_number = Field([none_if_blank(), optional(), max_length(100)])
    image_url = Field([none_if_blank(), optional(), url()])
    histological_summary = Field([none_if_blank(), optional(), max_length(10000)])
    em_findings = Field([none_if_blank(), optional(), max_length(10000)])

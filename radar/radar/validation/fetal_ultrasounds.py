from radar.validation.sources import SourceGroupValidationMixin
from radar.validation.core import Field, Validation
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, optional, range_, max_length, valid_date_for_patient, none_if_blank, in_
from radar.models.fetal_ultrasounds import LIQUOR_VOLUMES


class FetalUltrasoundValidation(PatientValidationMixin, SourceGroupValidationMixin, MetaValidationMixin, Validation):
    date_of_scan = Field([required(), valid_date_for_patient()])
    fetal_identifier = Field([optional(), max_length(30)])
    gestational_age = Field([required(), range_(8 * 7, 42 * 7, 'days')])
    head_centile = Field([optional(), range_(0, 100)])
    abdomen_centile = Field([optional(), range_(0, 100)])
    uterine_artery_notched = Field([optional()])
    liquor_volume = Field([optional(), in_(LIQUOR_VOLUMES.keys())])
    comments = Field([none_if_blank(), optional(), max_length(10000)])

from radar.validation.sources import SourceValidationMixin
from radar.validation.core import Field, Validation
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, optional, range_, none_if_blank, max_length, not_in_future


class FetalAnomalyScanValidation(PatientValidationMixin, SourceValidationMixin, MetaValidationMixin, Validation):
    date_of_scan = Field([required(), not_in_future()])
    gestational_age = Field([required(), range_(8 * 7, 42 * 7, 'days')])
    oligohydramnios = Field([optional()])
    right_anomaly_details = Field([none_if_blank(), optional(), max_length(10000)])
    right_ultrasound_details = Field([none_if_blank(), optional(), max_length(10000)])
    left_anomaly_details = Field([none_if_blank(), optional(), max_length(10000)])
    left_ultrasound_details = Field([none_if_blank(), optional(), max_length(10000)])

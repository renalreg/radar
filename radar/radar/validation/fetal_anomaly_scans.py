from radar.validation.data_sources import DataSourceValidationMixin
from radar.validation.core import Field, Validation
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, optional, min_, max_, none_if_blank, max_length


class FetalAnomalyScanValidation(PatientValidationMixin, DataSourceValidationMixin, MetaValidationMixin, Validation):
    date_of_scan = Field([required()])
    gestation_days = Field([required(), min_(8 * 7), max_(45 * 7)])
    oligohydramnios = Field([optional()])
    right_anomaly_details = Field([none_if_blank(), optional(), max_length(1000)])
    right_ultrasound_details = Field([none_if_blank(), optional(), max_length(1000)])
    left_anomaly_details = Field([none_if_blank(), optional(), max_length(1000)])
    left_ultrasound_details = Field([none_if_blank(), optional(), max_length(1000)])

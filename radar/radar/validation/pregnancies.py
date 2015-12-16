from radar.validation.core import Field, Validation
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, optional, range_, \
    valid_date_for_patient, in_, min_
from radar.models.pregnancies import OUTCOMES, DELIVERY_METHODS, PRE_ECLAMPSIA_TYPES


class PregnancyValidation(PatientValidationMixin, MetaValidationMixin, Validation):
    pregnancy_number = Field([required(), min_(1)])
    date_of_lmp = Field([required(), valid_date_for_patient()])
    gravidity = Field([optional(), range_(0, 9)])
    parity1 = Field([optional(), range_(0, 9)])
    parity2 = Field([optional(), range_(0, 9)])
    outcome = Field([optional(), in_(OUTCOMES.keys())])
    weight = Field([optional(), range_(200, 5000)])
    weight_centile = Field([optional(), range_(20, 90)])
    gestational_age = Field([optional(), range_(20 * 7, 42 * 7, 'days')])
    delivery_method = Field([optional(), DELIVERY_METHODS.keys()])
    neonatal_intensive_care = Field([optional()])
    pre_eclampsia = Field([optional(), in_(PRE_ECLAMPSIA_TYPES.keys())])

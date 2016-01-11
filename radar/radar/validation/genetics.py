from radar.validation.groups import CohortGroupValidationMixin
from radar.validation.core import Field, Validation
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, optional, max_length, \
    none_if_blank, valid_date_for_patient, in_
from radar.models.genetics import GENETICS_KARYOTYPES


class GeneticsValidation(PatientValidationMixin, CohortGroupValidationMixin, MetaValidationMixin, Validation):
    date_sent = Field([required(), valid_date_for_patient()])
    laboratory = Field([none_if_blank(), optional(), max_length(100)])
    reference_number = Field([none_if_blank(), optional(), max_length(100)])
    karyotype = Field([optional(), in_(GENETICS_KARYOTYPES.keys())])
    results = Field([none_if_blank(), optional(), max_length(10000)])
    summary = Field([none_if_blank(), optional(), max_length(10000)])

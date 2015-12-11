from radar.validation.cohorts import CohortValidationMixin
from radar.validation.core import Field, Validation
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, none_if_blank, optional, max_length, in_
from radar.validation.core import ListField
from radar.models.family_history import RELATIONSHIPS


class FamilyHistoryRelativeValidation(Validation):
    relationship = Field([required(), in_(RELATIONSHIPS.keys())])
    patient = Field([optional()])


class FamilyHistoryValidation(PatientValidationMixin, CohortValidationMixin, MetaValidationMixin, Validation):
    parental_consanguinity = Field([required()])
    family_history = Field([required()])
    other_family_history = Field([none_if_blank(), optional(), max_length(1000)])
    relatives = ListField(FamilyHistoryRelativeValidation())

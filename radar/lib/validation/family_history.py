from radar.lib.validation.core import Field, Validation
from radar.lib.validation.meta import MetaValidationMixin
from radar.lib.validation.patients import PatientValidationMixin
from radar.lib.validation.validators import required


class FamilyHistoryValidation(PatientValidationMixin, MetaValidationMixin, Validation):
    parental_consanguinity = Field([required()])
    family_history = Field([required()])

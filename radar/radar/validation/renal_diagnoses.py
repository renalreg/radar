from radar.validation.core import Field, Validation
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import optional, valid_date_for_patient


class RenalDiagnosisValidation(PatientValidationMixin, MetaValidationMixin, Validation):
    onset_date = Field([optional(), valid_date_for_patient()])
    esrf_date = Field([optional(), valid_date_for_patient()])

from radar.validation.core import Field, Validation, ValidationError, pass_new_obj
from radar.validation.sources import SourceGroupValidationMixin
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, optional, \
    valid_date_for_patient, in_
from radar.models.dialysis import DIALYSIS_MODALITIES


class DialysisValidation(PatientValidationMixin, SourceGroupValidationMixin, MetaValidationMixin, Validation):
    from_date = Field([required(), valid_date_for_patient()])
    to_date = Field([optional(), valid_date_for_patient()])
    modality = Field([required(), in_(DIALYSIS_MODALITIES.keys())])

    @pass_new_obj
    def validate_to_date(self, obj, to_date):
        if to_date < obj.from_date:
            raise ValidationError('Must be on or after from date.')

        return to_date

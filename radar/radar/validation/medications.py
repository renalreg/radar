from radar.models import MEDICATION_DOSE_UNITS, MEDICATION_FREQUENCIES, MEDICATION_ROUTES
from radar.validation.core import Field, Validation, ValidationError, pass_new_obj, pass_call
from radar.validation.sources import SourceValidationMixin
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import valid_date_for_patient, required, optional, not_empty, min_, in_, max_length, none_if_blank


class MedicationValidation(PatientValidationMixin, SourceValidationMixin, MetaValidationMixin, Validation):
    from_date = Field([required(), valid_date_for_patient()])
    to_date = Field([optional(), valid_date_for_patient()])
    drug = Field([optional()])
    dose_quantity = Field([optional(), min_(0)])
    dose_unit = Field([optional(), in_(MEDICATION_DOSE_UNITS.keys())])
    frequency = Field([optional(), in_(MEDICATION_FREQUENCIES.keys())])
    route = Field([optional(), in_(MEDICATION_ROUTES.keys())])
    drug_text = Field([none_if_blank(), optional(), max_length(10000)])
    dose_text = Field([none_if_blank(), optional(), max_length(10000)])

    def pre_validate(self, obj):
        if obj.drug:
            obj.drug_text = None

        return obj

    @pass_new_obj
    def validate_to_date(self, obj, to_date):
        if to_date < obj.from_date:
            raise ValidationError('Must be on or after from date.')

        return to_date

    @pass_call
    def validate(self, call, obj):
        # Must specify a drug
        if obj.drug is None and obj.drug_text is None:
            raise ValidationError({
                'drug': 'Must specify a drug.',
                'drug_text': 'Must specify a drug.',
            })

        # Dose unit is required when dose quantity is entered
        if obj.dose_quantity is not None:
            call.validators_for_field([required()], obj, self.dose_unit)

        return obj

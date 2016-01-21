from radar.validation.sources import SourceValidationMixin
from radar.validation.core import Field, Validation, ValidationError, pass_new_obj
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, optional, valid_date_for_patient, \
    max_length, none_if_blank, in_
from radar.models.diagnoses import BIOPSY_DIAGNOSES


# TODO
class DiagnosisValidation(Validation):
    pass


# TODO
class GroupDiagnosisValidation(Validation):
    pass


class PatientDiagnosisValidation(PatientValidationMixin, SourceValidationMixin, MetaValidationMixin, Validation):
    diagnosis = Field([optional()])
    diagnosis_text = Field([none_if_blank(), optional(), max_length(1000)])
    symptoms_date = Field([optional(), valid_date_for_patient()])
    from_date = Field([required(), valid_date_for_patient()])
    to_date = Field([optional(), valid_date_for_patient()])
    gene_test = Field([optional()])
    biochemistry = Field([optional()])
    clinical_picture = Field([optional()])
    biopsy = Field([optional()])
    biopsy_diagnosis = Field([optional(), in_(BIOPSY_DIAGNOSES.keys())])

    def pre_validate(self, obj):
        if obj.diagnosis is not None:
            obj.diagnosis_text = None

        if not obj.biopsy:
            obj.biopsy_diagnosis = None

        return obj

    @pass_new_obj
    def validate_from_date(self, obj, from_date):
        symptoms_date = obj.symptoms_date

        if symptoms_date is not None and from_date < symptoms_date:
            raise ValidationError('Must be on or after date of onset of symptoms.')

        return from_date

    @pass_new_obj
    def validate_to_date(self, obj, to_date):
        if to_date is not None and to_date < obj.from_date:
            raise ValidationError('Must be on or after from date.')

        return to_date

    def validate(self, obj):
        if obj.diagnosis is None and obj.diagnosis_text is None:
            raise ValidationError({
                'diagnosis': 'Must specify a diagnosis.',
                'diagnosis_text': 'Must specify a diagnosis.',
            })

        return obj

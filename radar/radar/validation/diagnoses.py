from radar.validation.groups import CohortGroupValidationMixin
from radar.validation.core import Field, Validation, ValidationError, pass_new_obj
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, optional, \
    valid_date_for_patient, max_length, none_if_blank


class DiagnosisValidation(PatientValidationMixin, CohortGroupValidationMixin, MetaValidationMixin, Validation):
    date_of_symptoms = Field([optional(), valid_date_for_patient()])
    date_of_diagnosis = Field([required(), valid_date_for_patient()])
    date_of_renal_disease = Field([optional(), valid_date_for_patient()])
    group_diagnosis = Field([optional()])  # TODO
    gene_test = Field([optional()])
    biochemistry = Field([optional()])
    clinical_picture = Field([optional()])
    biopsy = Field([optional()])
    biopsy_diagnosis = Field([optional()])  # TODO
    diagnosis_text = Field([none_if_blank(), optional(), max_length(10000)])

    @pass_new_obj
    def validate_date_of_diagnosis(self, obj, date_of_diagnosis):
        if date_of_diagnosis < obj.date_of_symptoms:
            raise ValidationError('Must be on or after date of onset of symptoms.')

        return date_of_diagnosis

    @pass_new_obj
    def validate_group_diagnosis(self, obj, group_diagnosis):
        if group_diagnosis.group != obj.group:
            raise ValidationError('Not a valid diagnosis for this cohort.')

        return group_diagnosis

    @pass_new_obj
    def validate_biopsy_diagnosis(self, obj, biopsy_diagnosis):
        if obj.group not in biopsy_diagnosis.groups:
            raise ValidationError('Not a valid biopsy diagnosis for this cohort.')

        return biopsy_diagnosis


class GroupDiagnosisValidation(CohortGroupValidationMixin, Validation):
    name = Field([required()])
    display_order = Field([required()])

from radar.lib.permissions import has_edit_patient_permission
from radar.lib.validation.core import Validation, Field, pass_context, pass_old_obj, ValidationError
from radar.lib.validation.meta import MetaValidationMixin
from radar.lib.validation.validators import required


class CohortPatientValidation(MetaValidationMixin, Validation):
    id = Field()
    cohort = Field([required()])
    patient = Field([required()])
    is_active = Field([required()])

    @pass_context
    @pass_old_obj
    def validate(self, ctx, old_obj, new_obj):
        current_user = ctx['user']

        # Permission for the new patient
        if not has_edit_patient_permission(new_obj.patient, current_user):
            raise ValidationError({'cohort': 'Permission denied!'})

        # Check that the patient doesn't already belong to this cohort
        new_cohort = new_obj.cohort
        duplicate = any(x != new_obj and x.cohort == new_cohort for x in new_obj.patient.cohort_patients)

        if duplicate:
            raise ValidationError({'cohort': 'Patient already belongs to this cohort.'})

        # Updating existing record
        if old_obj.id is not None:
            # Permission for the old patient (might have been updated)
            if not has_edit_patient_permission(old_obj.patient, current_user):
                raise ValidationError({'cohort': 'Permission denied!'})

        return new_obj

from radar.permissions import can_user_edit_patient
from radar.validation.core import Validation, Field, pass_context, pass_old_obj, ValidationError
from radar.validation.meta import MetaValidationMixin
from radar.validation.validators import required


class CohortPatientValidation(MetaValidationMixin, Validation):
    id = Field()
    cohort = Field([required()])
    patient = Field([required()])
    is_active = Field([required()])
    recruited_by_organisation = Field([required()])  # TODO validate

    @pass_context
    @pass_old_obj
    def validate(self, ctx, old_obj, new_obj):
        current_user = ctx['user']

        # Permission for the new patient
        if not can_user_edit_patient(current_user, new_obj.patient):
            raise ValidationError({'cohort': 'Permission denied!'})

        # Check that the patient doesn't already belong to this cohort
        new_cohort = new_obj.cohort
        duplicate = any(x != new_obj and x.cohort == new_cohort for x in new_obj.patient.cohort_patients)

        if duplicate:
            raise ValidationError({'cohort': 'Patient already belongs to this cohort.'})

        # Updating existing record
        if old_obj.id is not None:
            # Permission for the old patient (might have been updated)
            if not can_user_edit_patient(current_user, old_obj.patient):
                raise ValidationError({'cohort': 'Permission denied!'})

        return new_obj

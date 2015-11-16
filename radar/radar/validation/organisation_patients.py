from radar.validation.core import Validation, Field, pass_old_obj, pass_context, ValidationError
from radar.validation.meta import MetaValidationMixin
from radar.validation.validators import required
from radar.permissions import has_permission_for_organisation


class OrganisationPatientValidation(MetaValidationMixin, Validation):
    id = Field()
    organisation = Field([required()])
    patient = Field([required()])
    is_active = Field([required()])

    @staticmethod
    def has_permission(current_user, organisation):
        return (
            current_user.is_admin or
            has_permission_for_organisation(current_user, organisation, 'has_edit_patient_permission')
        )

    @pass_context
    @pass_old_obj
    def validate(self, ctx, old_obj, new_obj):
        current_user = ctx['user']

        new_organisation = new_obj.organisation

        # Check the current user has permission for the new organisation
        if not OrganisationPatientValidation.has_permission(current_user, new_organisation):
            raise ValidationError({'role': 'Permission denied!'})

        # Check that the patient doesn't already belong to this organisation
        # Note: it's important this check happens after the above permission check to prevent membership enumeration
        new_organisation = new_obj.organisation
        duplicate = any(x != new_obj and x.organisation == new_organisation for x in new_obj.patient.organisation_patients)

        if duplicate:
            raise ValidationError({'organisation': 'Patient already belongs to this organisation.'})

        # Updating an existing record
        if old_obj.id is not None:
            old_organisation = old_obj.organisation

            # Check the current user has permission for the old organisation
            if not OrganisationPatientValidation.has_permission(current_user, old_organisation):
                raise ValidationError({'organisation': 'Permission denied!'})

        return new_obj

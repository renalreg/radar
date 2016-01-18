from radar.validation.core import Validation, Field, pass_context, pass_old_obj, ValidationError
from radar.validation.meta import MetaValidationMixin
from radar.validation.validators import required, optional
from radar.permissions import has_permission_for_group, PERMISSION, has_permission_for_patient
from radar.exceptions import PermissionDenied


class GroupPatientValidation(MetaValidationMixin, Validation):
    id = Field()
    group = Field([required()])
    patient = Field([required()])
    from_date = Field([required()])
    to_date = Field([optional()])
    created_group = Field([optional()])  # TODO validate

    @classmethod
    def has_permission(cls, user, obj):
        return (
            has_permission_for_patient(user, obj.patient, PERMISSION.EDIT_PATIENT) and
            has_permission_for_group(user, obj.group, PERMISSION.EDIT_PATIENT)
        )

    @classmethod
    def is_duplicate(cls, obj):
        group = obj.group
        duplicate = any(x != obj and x.group == group for x in obj.patient.current_group_patients)
        return duplicate

    @pass_context
    @pass_old_obj
    def validate(self, ctx, old_obj, new_obj):
        current_user = ctx['user']

        # Updating existing record
        if old_obj.id is not None:
            # Check permissions on old membership
            if not self.has_permission(current_user, old_obj):
                raise PermissionDenied()

        # Check permissions on new membership
        if not self.has_permission(current_user, new_obj):
            raise PermissionDenied()

        # Check that the patient doesn't already belong to this group
        # Note: it's important this check happens after the permission checks to prevent membership enumeration
        if self.is_duplicate(new_obj):
            raise ValidationError({'group': 'Patient already belongs to this group.'})

        return new_obj

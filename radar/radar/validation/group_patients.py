from radar.validation.core import Validation, Field, pass_context, pass_old_obj, ValidationError, pass_call
from radar.validation.meta import MetaValidationMixin
from radar.validation.validators import required, optional
from radar.permissions import has_permission_for_group, PERMISSION, has_permission_for_patient
from radar.exceptions import PermissionDenied
from radar.models.groups import GROUP_TYPE


class GroupPatientValidation(MetaValidationMixin, Validation):
    id = Field()
    group = Field([required()])
    patient = Field([required()])
    from_date = Field([required()])
    to_date = Field([optional()])
    created_group = Field([required()])

    @classmethod
    def is_duplicate(cls, obj):
        group = obj.group
        duplicate = any(x != obj and x.group == group for x in obj.patient.current_group_patients)
        return duplicate

    @classmethod
    def check_permissions(cls, user, obj):
        # Check permissions on patient
        if not has_permission_for_patient(user, obj.patient, PERMISSION.VIEW_PATIENT):
            raise PermissionDenied()

        # Check group permissions
        if not (
            has_permission_for_group(user, obj.group, PERMISSION.EDIT_PATIENT_MEMBERSHIP, explicit=True) or
            (
                has_permission_for_group(user, obj.group, PERMISSION.EDIT_PATIENT_MEMBERSHIP) and
                has_permission_for_group(user, obj.created_group, PERMISSION.EDIT_PATIENT_MEMBERSHIP, explicit=True)
            )
        ):
            raise PermissionDenied()

    @pass_context
    @pass_call
    @pass_old_obj
    def validate(self, ctx, call, old_obj, new_obj):
        current_user = ctx['user']

        # Created group is required when the group is a cohort
        if new_obj.group.type == GROUP_TYPE.COHORT:
            call.validators_for_field([required()], new_obj, self.created_group)

        if old_obj.id is not None:
            # Check permissions on old membership
            self.check_permissions(current_user, old_obj)

        # Check permissions on new membership
        self.check_permissions(current_user, new_obj)

        # Check that the patient doesn't already belong to this group
        # Note: it's important this check happens after the permission checks to prevent membership enumeration
        if self.is_duplicate(new_obj):
            raise ValidationError({'group': 'Patient already belongs to this group.'})

        return new_obj

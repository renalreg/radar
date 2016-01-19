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
    created_group = Field([required()])

    @classmethod
    def is_duplicate(cls, obj):
        group = obj.group
        duplicate = any(x != obj and x.group == group for x in obj.patient.current_group_patients)
        return duplicate

    @pass_context
    @pass_old_obj
    def validate(self, ctx, old_obj, new_obj):
        current_user = ctx['user']

        if not has_permission_for_patient(current_user, new_obj.patient, PERMISSION.VIEW_PATIENT):
            raise PermissionDenied()

        if not has_permission_for_group(current_user, new_obj.group, PERMISSION.EDIT_PATIENT_MEMBERSHIP):
            raise PermissionDenied()

        check_old_created_group = (
            old_obj.id is not None and
            old_obj.created_group != new_obj.created_group
        )

        check_new_created_group = (
            old_obj.id is None or
            old_obj.group != new_obj.group or
            old_obj.created_group != new_obj.created_group
        )

        if (
            check_old_created_group and
            not has_permission_for_group(
                current_user,
                old_obj.created_group,
                PERMISSION.EDIT_PATIENT_MEMBERSHIP,
                explicit=True
            )
        ) or (
            check_new_created_group and
            not has_permission_for_group(
                current_user,
                new_obj.created_group,
                PERMISSION.EDIT_PATIENT_MEMBERSHIP,
                explicit=True
            )
        ):
            raise PermissionDenied()

        # Check that the patient doesn't already belong to this group
        # Note: it's important this check happens after the permission checks to prevent membership enumeration
        if self.is_duplicate(new_obj):
            raise ValidationError({'group': 'Patient already belongs to this group.'})

        return new_obj

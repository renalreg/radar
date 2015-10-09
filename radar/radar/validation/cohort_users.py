from radar.roles import COHORT_ROLES
from radar.validation.core import Validation, Field, pass_old_obj, ValidationError, pass_context
from radar.validation.meta import MetaValidationMixin
from radar.validation.validators import required, in_


class CohortUserValidation(MetaValidationMixin, Validation):
    id = Field()
    cohort = Field([required()])
    user = Field([required()])
    role = Field([required(), in_(COHORT_ROLES.keys())])

    @staticmethod
    def has_permission(current_user, cohort, role):
        if current_user.is_admin:
            grant = True
        else:
            grant = False

            for cohort_user in current_user.cohort_users:
                if cohort_user.cohort == cohort:
                    if role in cohort_user.managed_roles:
                        grant = True

                    break

        return grant

    @pass_context
    @pass_old_obj
    def validate(self, ctx, old_obj, new_obj):
        current_user = ctx['user']

        new_user = new_obj.user

        # Can't change your own role
        if new_user == current_user and not current_user.is_admin:
            raise ValidationError({'cohort': 'Permission denied!'})

        new_role = new_obj.role
        new_cohort = new_obj.cohort

        # Check the current user has permission for the new cohort and role
        if not CohortUserValidation.has_permission(current_user, new_cohort, new_role):
            raise ValidationError({'role': 'Permission denied!'})

        # Check that the user doesn't already belong to this cohort
        new_cohort = new_obj.cohort
        duplicate = any(x != new_obj and x.cohort == new_cohort for x in new_obj.user.cohort_users)

        # Note: it's important this check happens after the above permission check to prevent membership enumeration
        if duplicate:
            raise ValidationError({'cohort': 'User already belongs to this cohort.'})

        # Updating existing record
        if old_obj.id is not None:
            old_user = old_obj.user

            # Can't change your own role
            if old_user == current_user and not current_user.is_admin:
                raise ValidationError({'cohort': 'Permission denied!'})

            old_role = old_obj.role
            old_cohort = old_obj.cohort

            # Check the current user has permission for the old cohort and role
            if not CohortUserValidation.has_permission(current_user, old_cohort, old_role):
                raise ValidationError({'role': 'Permission denied!'})

        return new_obj

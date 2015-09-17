from radar.lib.roles import ORGANISATION_ROLES
from radar.lib.validation.core import Validation, Field, pass_context, pass_old_obj, ValidationError
from radar.lib.validation.meta import MetaValidationMixin
from radar.lib.validation.validators import required, in_


class OrganisationUserValidation(MetaValidationMixin, Validation):
    id = Field()
    organisation = Field([required()])
    user = Field([required()])
    role = Field([required(), in_(ORGANISATION_ROLES.keys())])

    @staticmethod
    def has_permission(current_user, organisation, role):
        if current_user.is_admin:
            grant = True
        else:
            grant = False

            for organisation_user in current_user.organisation_users:
                if organisation_user.organisation == organisation:
                    if role in organisation_user.managed_roles:
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
            raise ValidationError({'user': 'Permission denied!'})

        new_role = new_obj.role
        new_organisation = new_obj.organisation

        # Check the current user has permission for the new organisation and role
        if not OrganisationUserValidation.has_permission(current_user, new_organisation, new_role):
            raise ValidationError({'role': 'Permission denied!'})

        # Check that the user doesn't already belong to this organisation
        new_organisation = new_obj.organisation
        duplicate = any(x != new_obj and x.organisation == new_organisation for x in new_obj.user.organisation_users)

        # Note: it's important this check happens after the above permission check to prevent membership enumeration
        if duplicate:
            raise ValidationError({'organisation': 'User already belongs to this organisation.'})

        # Updating an existing record
        if old_obj.id is not None:
            old_user = old_obj.user

            # Can't change your own role
            if old_user == current_user and not current_user.is_admin:
                raise ValidationError({'user': 'Permission denied!'})

            old_role = old_obj.role
            old_organisation = old_obj.organisation

            # Check the current user has permission for the old organisation and role
            if not OrganisationUserValidation.has_permission(current_user, old_organisation, old_role):
                raise ValidationError({'role': 'Permission denied!'})

        return new_obj

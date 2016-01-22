from radar.roles import ROLE
from radar.validation.core import Validation, Field, pass_old_obj, ValidationError, pass_context
from radar.validation.meta import MetaValidationMixin
from radar.validation.validators import required, in_
from radar.permissions import has_permission_for_group_role
from radar.exceptions import PermissionDenied


class GroupUserValidation(MetaValidationMixin, Validation):
    id = Field()
    group = Field([required()])
    user = Field([required()])
    role = Field([required(), in_(ROLE)])

    @classmethod
    def check_permissions(cls, user, obj):
        # Can't change your own role
        if user == obj.user and not user.is_admin:
            raise PermissionDenied()

        # Check the user has permission for the group and role
        if not has_permission_for_group_role(user, obj.group, obj.role):
            raise PermissionDenied()

    @classmethod
    def is_duplicate(cls, obj):
        group = obj.group
        role = obj.role
        duplicate = any(x != obj and x.group == group and x.role == role for x in obj.user.group_users)
        return duplicate

    @pass_context
    @pass_old_obj
    def validate(self, ctx, old_obj, new_obj):
        current_user = ctx['user']

        # Updating existing record
        if old_obj.id is not None:
            self.check_permissions(current_user, old_obj)

        self.check_permissions(current_user, new_obj)

        # Check that the user doesn't already belong to this group
        # Note: it's important this check happens after the above permission check to prevent membership enumeration
        if self.is_duplicate(new_obj):
            raise ValidationError({'group': 'User already belongs to this group.'})

        return new_obj

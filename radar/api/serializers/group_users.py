from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake.exceptions import ValidationError

from radar.api.serializers.common import (
    UserMixin,
    MetaMixin,
    GroupField,
    EnumLookupField
)
from radar.exceptions import PermissionDenied
from radar.models.groups import GroupUser
from radar.permissions import has_permission_for_group_role
from radar.roles import ROLE, ROLE_NAMES


class GroupUserSerializer(UserMixin, MetaMixin, ModelSerializer):
    group = GroupField()
    role = EnumLookupField(ROLE, ROLE_NAMES)

    class Meta(object):
        model_class = GroupUser
        exclude = ['group_id']

    def check_permissions(self, user, group, role):
        current_user = self.context['user']

        # Can't change your own role
        if current_user == user and not current_user.is_admin:
            raise PermissionDenied()

        # Check the user has permission for the group and role
        if not has_permission_for_group_role(current_user, group, role):
            raise PermissionDenied()

    def is_duplicate(self, data):
        group = data['group']
        user = data['user']
        instance = self.instance

        duplicate = any(
            group == x.group and
            (instance is None or instance != x)
            for x in user.group_users
        )

        return duplicate

    def validate(self, data):
        data = super(GroupUserSerializer, self).validate(data)

        instance = self.instance

        # Updating existing record
        if instance is not None:
            self.check_permissions(instance.user, instance.group, instance.role)

        self.check_permissions(data['user'], data['group'], data['role'])

        # Check that the user doesn't already belong to this group
        # Note: it's important this check happens after the above permission check to prevent membership enumeration
        if self.is_duplicate(data):
            raise ValidationError({'group': 'User already belongs to this group.'})

        return data

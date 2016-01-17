from radar.validation.core import ValidationError, pass_context
from radar.validation.core import Field
from radar.validation.validators import required
from radar.permissions import has_permission_for_group, has_permission
from radar.roles import PERMISSION
from radar.groups import is_radar_group
from radar.models.source_types import SOURCE_TYPE_RADAR
from radar.models.groups import GROUP_TYPE_HOSPITAL


class SourceGroupField(Field):
    @pass_context
    def validate(self, ctx, group):
        user = ctx['user']

        if not user.is_admin and not is_radar_group(group) and group.type != GROUP_TYPE_HOSPITAL:
            raise ValidationError('Must be RaDaR or a hospital.')

        if not has_permission_for_group(user, group, PERMISSION.EDIT_PATIENT):
            raise ValidationError('Permission denied!')

        return group


class RadarSourceGroupField(Field):
    @pass_context
    def validate(self, ctx, group):
        user = ctx['user']

        if not user.is_admin and not is_radar_group(group):
            raise ValidationError('Must be RaDaR.')

        if not has_permission_for_group(user, group, PERMISSION.EDIT_PATIENT):
            raise ValidationError('Permission denied!')

        return group


class SourceTypeField(Field):
    def pre_validate(self, source_type):
        # Default to the RaDaR source type if missing
        if source_type is None:
            source_type = SOURCE_TYPE_RADAR

        return source_type

    @pass_context
    def validate(self, ctx, source_type):
        user = ctx['user']

        # Only admins can enter data for a non-RaDaR source type
        if not user.is_admin and source_type != SOURCE_TYPE_RADAR:
            raise ValidationError('Permission denied!')

        return source_type


class SourceValidationMixin(object):
    source_group = SourceGroupField([required()])
    source_type = SourceTypeField([required()])


class RadarSourceValidationMixin(object):
    source_group = RadarSourceGroupField([required()])
    source_type = SourceTypeField([required()])

from radar.validation.core import ValidationError, pass_context
from radar.validation.core import Field
from radar.validation.validators import required
from radar.permissions import has_permission_for_group
from radar.roles import PERMISSIONS
from radar.groups import is_radar_group
from radar.source_types import is_radar_source_type, get_radar_source_type


class SourceGroupField(Field):
    @pass_context
    def validate(self, ctx, group):
        user = ctx['user']

        if not user.is_admin or not has_permission_for_group(user, group, PERMISSIONS.EDIT_PATIENT):
            raise ValidationError('Permission denied!')

        return group


class RadarSourceGroupField(Field):
    @pass_context
    def validate(self, ctx, group):
        user = ctx['user']

        if not user.is_admin and not is_radar_group(group):
            raise ValidationError('Permission denied!')

        return group


class SourceTypeField(Field):
    def pre_validate(self, source_type):
        # Default to the RaDaR source type if missing
        if source_type is None:
            source_type = get_radar_source_type()

        return source_type

    @pass_context
    def validate(self, ctx, source_type):
        user = ctx['user']

        # Only admins can enter data for a non-RaDaR source type
        if not user.is_admin and not is_radar_source_type(source_type):
            raise ValidationError('Permission denied!')

        return source_type


class SourceValidationMixin(object):
    source_group = SourceGroupField([required()])
    source_type = SourceTypeField([required()])


class RadarSourceValidationMixin(object):
    source_group = RadarSourceGroupField([required()])
    source_type = SourceTypeField([required()])

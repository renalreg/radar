from radar.validation.core import ValidationError, pass_context
from radar.validation.core import Field
from radar.validation.validators import required
from radar.permissions import has_permission_for_group
from radar.roles import PERMISSIONS
from radar.groups import is_radar_group
from radar.sources import is_radar_source


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


class SourceField(Field):
    @pass_context
    def validate(self, ctx, source):
        user = ctx['user']

        if not user.is_admin and not is_radar_source(source):
            raise ValidationError('Permission denied!')

        return source


class SourceGroupValidationMixin(object):
    source_group = SourceGroupField([required()])
    source = SourceField()


class RadarSourceGroupValidationMixin(object):
    source_group = RadarSourceGroupField([required()])
    source = SourceField()

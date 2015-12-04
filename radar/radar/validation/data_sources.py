from radar.data_sources import DATA_SOURCE_TYPE_RADAR, is_radar_data_source
from radar.validation.core import ValidationError, pass_context, Validation
from radar.validation.core import Field
from radar.validation.validators import required
from radar.permissions import has_permission_for_organisation
from radar.roles import PERMISSIONS


# TODO
class DataSourceValidation(Validation):
    pass


class DataSourceField(Field):
    @pass_context
    def validate(self, ctx, data_source):
        def deny():
            raise ValidationError('Permission denied!')

        user = ctx['user']

        if not user.is_admin:
            if data_source.type != DATA_SOURCE_TYPE_RADAR:
                deny()

            organisation = data_source.organisation

            if not has_permission_for_organisation(user, organisation, PERMISSIONS.EDIT_PATIENT):
                deny()

        return data_source


class RadarDataSourceField(Field):
    @pass_context
    def validate(self, ctx, data_source):
        user = ctx['user']

        if not user.is_admin and not is_radar_data_source(data_source):
            raise ValidationError('Permission denied!')

        return data_source


class DataSourceValidationMixin(object):
    data_source = DataSourceField([required()])


class RadarDataSourceValidationMixin(object):
    data_source = RadarDataSourceField([required()])

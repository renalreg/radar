from radar.lib.data_sources import DATA_SOURCE_TYPE_RADAR, is_radar_data_source
from radar.lib.validation.core import ValidationError, pass_context, Validation, pass_call
from radar.lib.validation.core import Field
from radar.lib.validation.meta import MetaValidationMixin
from radar.lib.validation.validators import required


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

            grant = False

            data_source_organisation = data_source.organisation

            for organisation_user in user.organisation_users:
                if organisation_user == data_source_organisation and organisation_user.has_edit_patient_permission:
                    grant = True
                    break

            if not grant:
                deny()

        return data_source


class RadarDataSourceField(Field):
    @pass_context
    def validate(self, ctx, data_source):
        user = ctx['user']

        if not user.is_admin and not is_radar_data_source(data_source.data_source):
            raise ValidationError('Permission denied!')

        return data_source


class DataSourceValidationMixin(object):
    data_source = DataSourceField([required()])


class RadarDataSourceValidationMixin(object):
    data_source = RadarDataSourceField([required()])

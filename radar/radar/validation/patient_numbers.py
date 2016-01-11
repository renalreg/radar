from radar.models import GROUP_TYPE_OTHER
from radar.groups import is_radar_group
from radar.validation.core import Validation, pass_call, ValidationError, Field
from radar.validation.data_sources import RadarDataSourceValidationMixin
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, max_length, not_empty, normalise_whitespace
from radar.validation.number_validators import NUMBER_VALIDATORS


class PatientNumberValidation(PatientValidationMixin, RadarDataSourceValidationMixin, MetaValidationMixin, Validation):
    group = Field([required()])
    number = Field([not_empty(), normalise_whitespace(), max_length(50)])

    def validate_group(self, group):
        if is_radar_group(group):
            raise ValidationError("Can't add RaDaR numbers.")

        return group

    @pass_call
    def validate(self, call, obj):
        group = obj.group

        if group.type == GROUP_TYPE_OTHER:
            number_validators = NUMBER_VALIDATORS.get(group.code)

            if number_validators is not None:
                call.validators_for_field(number_validators, obj, self.number)

        return obj

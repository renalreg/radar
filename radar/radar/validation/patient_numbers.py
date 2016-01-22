from radar.groups import is_radar_group
from radar.validation.core import Validation, pass_call, ValidationError, Field
from radar.validation.sources import RadarSourceValidationMixin
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, max_length, not_empty, normalise_whitespace
from radar.validation.number_validators import NUMBER_VALIDATORS


class PatientNumberValidation(PatientValidationMixin, RadarSourceValidationMixin, MetaValidationMixin, Validation):
    number = Field([not_empty(), normalise_whitespace(), max_length(50)])
    number_group = Field([required()])

    def validate_number_group(self, number_group):
        if is_radar_group(number_group):
            raise ValidationError("Can't add RaDaR numbers.")

        return number_group

    @pass_call
    def validate(self, call, obj):
        number_group = obj.number_group

        number_validators = NUMBER_VALIDATORS.get((number_group.type, number_group.code))

        if number_validators is not None:
            call.validators_for_field(number_validators, obj, self.number)

        return obj

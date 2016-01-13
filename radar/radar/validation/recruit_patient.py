from radar.validation.core import Validation, Field, pass_call, pass_context, ValidationError
from radar.validation.validators import optional, required, not_in_future, in_, none_if_blank
from radar.models.patients import GENDERS, ETHNICITIES
from radar.permissions import has_permission_for_group
from radar.groups import is_radar_group
from radar.validation.number_validators import NUMBER_VALIDATORS
from radar.roles import PERMISSION
from radar.models.groups import GROUP_TYPE_HOSPITAL


class RecruitPatientSearchValidation(Validation):
    first_name = Field([required()])
    last_name = Field([required()])
    date_of_birth = Field([required()])
    number = Field([required()])
    number_group = Field([required()])

    def validate_number_group(self, number_group):
        if not number_group.recruitment:
            raise ValidationError("Not a valid group.")

        return number_group

    @pass_call
    def validate(self, call, obj):
        number_group = obj['number_group']

        number_validators = NUMBER_VALIDATORS.get((number_group.type, number_group.code))

        if number_validators is not None:
            call.validators_for_field(number_validators, obj, self.number)

        return obj


def get_radar_id(obj):
    for x in obj['patient_numbers']:
        if is_radar_group(x['group']):
            return int(x['number'])

    return None


# TODO validate patient numbers
class RecruitPatientValidation(Validation):
    first_name = Field([none_if_blank(), optional()])
    last_name = Field([none_if_blank(), optional()])
    date_of_birth = Field([optional(), not_in_future()])
    gender = Field([optional(), in_(GENDERS.keys())])
    ethnicities = Field([optional(), in_(ETHNICITIES.keys())])
    recruited_group = Field([required()])
    group = Field([required()])

    @pass_context
    def validate_recruited_group(self, ctx, recruited_group):
        current_user = ctx['user']

        if not has_permission_for_group(current_user, recruited_group, PERMISSION.RECRUIT_PATIENT):
            raise ValidationError('PERMISSION denied!')

        if recruited_group.type != GROUP_TYPE_HOSPITAL:
            raise ValidationError('Must be a hospital.')

        return recruited_group

    @pass_call
    def validate(self, call, obj):
        radar_id = get_radar_id(obj)

        if radar_id is None:
            call.validators_for_field([required()], obj, self.first_name)
            call.validators_for_field([required()], obj, self.last_name)
            call.validators_for_field([required()], obj, self.date_of_birth)
            call.validators_for_field([required()], obj, self.gender)

        return obj

from radar.validation.core import Validation, Field, pass_call, pass_context, ValidationError
from radar.validation.validators import optional, required, not_in_future, in_, none_if_blank
from radar.models.patients import GENDERS
from radar.permissions import has_permission_for_organisation
from radar.organisations import is_radar_organisation
from radar.models.organisations import ORGANISATION_TYPE_OTHER
from radar.validation.patient_number_validators import NUMBER_VALIDATORS


class RecruitPatientSearchValidation(Validation):
    first_name = Field([required()])
    last_name = Field([required()])
    date_of_birth = Field([required()])
    number = Field([required()])
    number_organisation = Field([required()])

    def validate_number_organisation(self, number_organisation):
        if not number_organisation.is_national:
            raise ValidationError("Not a valid organisation.")

        return number_organisation

    @pass_call
    def validate(self, call, obj):
        number_organisation = obj['number_organisation']

        if number_organisation.type == ORGANISATION_TYPE_OTHER:
            number_validators = NUMBER_VALIDATORS.get(number_organisation.code)

            if number_validators is not None:
                call.validators_for_field(number_validators, obj, self.number)

        return obj


def get_radar_id(obj):
    for x in obj['patient_numbers']:
        if is_radar_organisation(x['organisation']):
            return int(x['number'])

    return None


# TODO validate patient numbers
class RecruitPatientValidation(Validation):
    first_name = Field([none_if_blank(), optional()])
    last_name = Field([none_if_blank(), optional()])
    date_of_birth = Field([optional(), not_in_future()])
    gender = Field([optional(), in_(GENDERS.keys())])
    ethnicity_code = Field([optional()])
    recruited_by_organisation = Field([required()])
    cohort = Field([required()])

    @pass_context
    def validate_recruited_by_organisation(self, ctx, recruited_by_organisation):
        current_user = ctx['user']

        if not has_permission_for_organisation(current_user, recruited_by_organisation, 'has_recruit_patient_permission'):
            raise ValidationError('Permission denied!')

        return recruited_by_organisation

    @pass_call
    def validate(self, call, obj):
        radar_id = get_radar_id(obj)

        if radar_id is None:
            call.validators_for_field([required()], obj, self.first_name)
            call.validators_for_field([required()], obj, self.last_name)
            call.validators_for_field([required()], obj, self.date_of_birth)
            call.validators_for_field([required()], obj, self.gender)

        return obj

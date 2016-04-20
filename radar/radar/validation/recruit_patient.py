from radar.validation.core import Validation, Field, pass_call, pass_context, ValidationError
from radar.validation.validators import optional, required, not_in_future, in_, not_empty, upper
from radar.models.patients import GENDERS, ETHNICITIES
from radar.permissions import has_permission_for_group
from radar.validation.number_validators import NUMBER_VALIDATORS
from radar.roles import PERMISSION
from radar.models.groups import GROUP_TYPE
from radar.exceptions import PermissionDenied


def get_number_validators(number_group):
    return NUMBER_VALIDATORS.get((number_group.type, number_group.code))


class RecruitPatientSearchValidation(Validation):
    first_name = Field([not_empty(), upper()])
    last_name = Field([not_empty(), upper()])
    date_of_birth = Field([required(), not_in_future()])
    gender = Field([required(), in_(GENDERS.keys())])
    number = Field([not_empty()])
    number_group = Field([required()])

    def validate_number_group(self, number_group):
        # Group must have the is_recruitment_number_group flag set
        if not number_group.is_recruitment_number_group:
            raise ValidationError('Patient number not suitable for recruitment.')

        return number_group

    @pass_call
    def validate(self, call, obj):
        number_group = obj['number_group']

        number_validators = get_number_validators(number_group)

        if number_validators is not None:
            call.validators_for_field(number_validators, obj, self.number)

        return obj


class RecruitPatientValidation(RecruitPatientSearchValidation):
    ethnicity = Field([optional(), in_(ETHNICITIES.keys())])
    cohort_group = Field([required()])
    hospital_group = Field([required()])

    @pass_context
    def validate_cohort_group(self, ctx, cohort_group):
        current_user = ctx['user']

        # Must have the RECRUIT_PATIENT permission on the cohort (this can be granted through hospital permissions)
        if not has_permission_for_group(current_user, cohort_group, PERMISSION.RECRUIT_PATIENT):
            raise PermissionDenied()

        # Group must be a cohort
        if cohort_group.type != GROUP_TYPE.COHORT:
            raise ValidationError('Must be a cohort.')

        # Check this is a recruitment group
        if not cohort_group.is_recruitment_group:
            raise ValidationError('Cannot recruit into this cohort.')

        return cohort_group

    @pass_context
    def validate_hospital_group(self, ctx, hospital_group):
        current_user = ctx['user']

        # Must have the RECRUIT_PATIENT permission on the hospital
        if not has_permission_for_group(current_user, hospital_group, PERMISSION.RECRUIT_PATIENT, explicit=True):
            raise PermissionDenied()

        # Group must be a hospital
        if hospital_group.type != GROUP_TYPE.HOSPITAL:
            raise ValidationError('Must be a hospital.')

        return hospital_group

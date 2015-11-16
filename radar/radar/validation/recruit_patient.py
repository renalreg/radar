from radar.validation.core import Validation, Field, pass_call, pass_context, ValidationError
from radar.validation.validators import optional, required, not_in_future, in_, none_if_blank
from radar.validation.patient_number_validators import nhs_no, ukrdc_no, chi_no
from radar.models.patients import GENDERS
from radar.permissions import has_permission_for_organisation


class RecruitPatientValidation(Validation):
    mpiid = Field([optional(), ukrdc_no()])
    radar_id = Field([optional()])
    recruited_by_organisation = Field([required()])
    cohort = Field([required()])
    first_name = Field([none_if_blank(), optional()])
    last_name = Field([none_if_blank(), optional()])
    date_of_birth = Field([optional(), not_in_future()])
    gender = Field([optional(), in_(GENDERS.keys())])
    nhs_no = Field([none_if_blank(), optional(), nhs_no()])
    chi_no = Field([none_if_blank(), optional(), chi_no()])

    @pass_context
    def validate_recruited_by_organisation(self, ctx, recruited_by_organisation):
        current_user = ctx['user']

        if not has_permission_for_organisation(current_user, recruited_by_organisation, 'has_recruit_patient_permission'):
            raise ValidationError('Permission denied!')

        return recruited_by_organisation

    @pass_call
    def validate(self, call, obj):
        if obj['radar_id'] is None:
            call.validators_for_field([required()], obj, self.first_name)
            call.validators_for_field([required()], obj, self.last_name)
            call.validators_for_field([required()], obj, self.date_of_birth)
            call.validators_for_field([required()], obj, self.gender)

        return obj

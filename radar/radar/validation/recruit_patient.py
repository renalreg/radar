from radar.validation.core import Validation, Field, pass_call
from radar.validation.validators import optional, required, not_empty, not_in_future, in_, none_if_blank
from radar.validation.patient_number_validators import nhs_no, ukrdc_no, chi_no
from radar.models.patients import GENDERS


class RecruitPatientValidation(Validation):
    mpiid = Field([optional(), ukrdc_no()])
    radar_id = Field([optional()])
    recruited_by_organisation = Field([required()])
    cohort = Field([required()])
    first_name = Field([optional()])
    last_name = Field([optional()])
    date_of_birth = Field([optional()])
    gender = Field([optional()])
    nhs_no = Field([optional()])
    chi_no = Field([optional()])

    @pass_call
    def validate(self, call, obj):
        if obj['radar_id'] is None:
            call.validators_for_field([not_empty()], obj, self.first_name)
            call.validators_for_field([not_empty()], obj, self.last_name)
            call.validators_for_field([required(), not_in_future()], obj, self.date_of_birth)
            call.validators_for_field([required(), in_(GENDERS.keys())], obj, self.gender)
            call.validators_for_field([none_if_blank(), optional(), nhs_no()], obj, self.nhs_no)
            call.validators_for_field([none_if_blank(), optional(), chi_no()], obj, self.chi_no)

        return obj

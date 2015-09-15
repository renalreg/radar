from radar.lib.organisations import is_chi_organisation, is_nhs_organisation, is_ukrr_organisation, \
    is_handc_organisation, is_radar_organisation
from radar.lib.validation.core import Validation, pass_call, ValidationError, Field
from radar.lib.validation.data_sources import DataSourceValidationMixin
from radar.lib.validation.patients import PatientValidationMixin
from radar.lib.validation.validators import required, max_length, not_empty, nhs_no, chi_no, ukrr_no, \
    normalise_whitespace, handc_no


class PatientNumberValidation(PatientValidationMixin, DataSourceValidationMixin, Validation):
    organisation = Field([required()])
    number = Field([not_empty(), normalise_whitespace(), max_length(50)])

    def validate_organisation(self, organisation):
        if is_radar_organisation(organisation):
            raise ValidationError("Can't add RaDaR numbers.")

        return organisation

    @pass_call
    def validate(self, call, obj):
        organisation = obj.organisation

        print self.number
        print self.number.chain

        if is_nhs_organisation(organisation):
            call.validators_for_field([nhs_no()], obj, self.number)
        elif is_chi_organisation(organisation):
            call.validators_for_field([chi_no()], obj, self.number)
        elif is_handc_organisation(organisation):
            call.validators_for_field([handc_no()], obj, self.number)
        elif is_ukrr_organisation(organisation):
            call.validators_for_field([ukrr_no()], obj, self.number)

        return obj

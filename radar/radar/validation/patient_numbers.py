from radar.models import ORGANISATION_CODE_NHS, ORGANISATION_CODE_CHI, ORGANISATION_CODE_HANDC, \
    ORGANISATION_CODE_UKRR, ORGANISATION_CODE_UKRDC, ORGANISATION_CODE_BAPN, ORGANISATION_TYPE_OTHER
from radar.organisations import is_radar_organisation
from radar.validation.core import Validation, pass_call, ValidationError, Field
from radar.validation.data_sources import RadarDataSourceValidationMixin
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, max_length, not_empty, normalise_whitespace
from radar.validation.patient_number_validators import nhs_no, chi_no, ukrr_no, handc_no, bapn_no, ukrdc_no


NUMBER_VALIDATORS = {
    ORGANISATION_CODE_NHS: [nhs_no()],
    ORGANISATION_CODE_CHI: [chi_no()],
    ORGANISATION_CODE_HANDC: [handc_no()],
    ORGANISATION_CODE_UKRR: [ukrr_no()],
    ORGANISATION_CODE_UKRDC: [ukrdc_no()],
    ORGANISATION_CODE_BAPN: [bapn_no()]
}


class PatientNumberValidation(PatientValidationMixin, RadarDataSourceValidationMixin, MetaValidationMixin, Validation):
    organisation = Field([required()])
    number = Field([not_empty(), normalise_whitespace(), max_length(50)])

    def validate_organisation(self, organisation):
        if is_radar_organisation(organisation):
            raise ValidationError("Can't add RaDaR numbers.")

        return organisation

    @pass_call
    def validate(self, call, obj):
        organisation = obj.organisation

        if organisation.type == ORGANISATION_TYPE_OTHER:
            number_validators = NUMBER_VALIDATORS.get(organisation.code)

            if number_validators is not None:
                call.validators_for_field(number_validators, obj, self.number)

        return obj

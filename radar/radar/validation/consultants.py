from radar.validation.core import Field, Validation, ListField
from radar.validation.meta import MetaValidationMixin
from radar.validation.validators import not_empty, none_if_blank, optional, email_address, max_length, required, upper
from radar.validation.number_validators import gmc_number


class OrganisationConsultantValidation(MetaValidationMixin, Validation):
    organisation = Field([required()])


class ConsultantValidation(MetaValidationMixin, Validation):
    title = Field([not_empty(), max_length(30)])
    first_name = Field([not_empty(), upper(), max_length(100)])
    last_name = Field([not_empty(), upper(), max_length(100)])
    email = Field([none_if_blank(), optional(), email_address()])
    telephone_number = Field([none_if_blank(), optional(), max_length(100)])
    gmc_number = Field([optional(), gmc_number()])
    organisation_consultants = ListField(OrganisationConsultantValidation())

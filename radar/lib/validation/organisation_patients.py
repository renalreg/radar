from radar.lib.validation.core import Validation, Field
from radar.lib.validation.meta import MetaValidationMixin
from radar.lib.validation.validators import required


# TODO
class OrganisationPatientValidation(MetaValidationMixin, Validation):
    organisation = Field([required()])
    patient = Field([required()])

from radar.lib.models import PLASMAPHERESIS_RESPONSES, PLASMAPHERESIS_NO_OF_EXCHANGES
from radar.lib.validation.core import Field, Validation, ValidationError, pass_new_obj
from radar.lib.validation.data_sources import DataSourceValidationMixin
from radar.lib.validation.meta import MetaValidationMixin
from radar.lib.validation.patients import PatientValidationMixin
from radar.lib.validation.validators import valid_date_for_patient, required, optional, in_


class PlasmapheresisValidation(PatientValidationMixin, DataSourceValidationMixin, MetaValidationMixin, Validation):
    from_date = Field([required(), valid_date_for_patient()])
    to_date = Field([optional(), valid_date_for_patient()])
    no_of_exchanges = Field([optional(), in_(PLASMAPHERESIS_NO_OF_EXCHANGES.keys())])
    response = Field([optional(), in_(PLASMAPHERESIS_RESPONSES.keys())])

    @pass_new_obj
    def validate_to_date(self, obj, to_date):
        if to_date < obj.from_date:
            raise ValidationError('Must be on or after from date.')

        return to_date

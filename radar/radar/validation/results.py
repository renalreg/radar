from radar.validation.core import Validation, Field, pass_new_obj, pass_call
from radar.validation.sources import SourceValidationMixin
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, min_, max_, min_length, max_length, in_
from radar.models.results import OBSERVATION_VALUE_TYPE


class ResultValidation(PatientValidationMixin, SourceValidationMixin, MetaValidationMixin, Validation):
    observation = Field([required()])
    date = Field([required()])  # TODO valid_date_for_patient()
    value = Field([required()])

    @pass_call
    @pass_new_obj
    def validate_value(self, call, obj, value):
        observation = obj.observation
        value_type = observation.value_type
        properties = observation.properties

        validators = []

        if value_type == OBSERVATION_VALUE_TYPE.INTEGER or value_type == OBSERVATION_VALUE_TYPE.REAL:
            min_value = properties.get('min_value')
            max_value = properties.get('max_value')

            if min_value is not None:
                validators.append(min_(min_value))

            if max_value is not None:
                validators.append(max_(max_value))
        elif value_type == OBSERVATION_VALUE_TYPE.ENUM:
            codes = [x['code'] for x in properties['options']]
            validators.append(in_(codes))
        elif value_type == OBSERVATION_VALUE_TYPE.STRING:
            min_length_value = properties.get('min_length')
            max_length_value = properties.get('max_length')

            if min_length_value is not None:
                validators.append(min_length(min_length_value))

            if max_length_value is not None:
                validators.append(max_length(max_length_value))

        value = call.validators(validators, value)

        return value

from radar.validation.core import Validation, Field, pass_new_obj, pass_call
from radar.validation.data_sources import DataSourceValidationMixin
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, min_, max_, min_length, max_length, in_
from radar.models.results import OBSERVATION_TYPE_INTEGER, OBSERVATION_TYPE_REAL,\
    OBSERVATION_TYPE_LOOKUP, OBSERVATION_TYPE_STRING


class ResultValidation(PatientValidationMixin, DataSourceValidationMixin, MetaValidationMixin, Validation):
    observation = Field([required()])
    date = Field([required()])  # TODO valid_date_for_patient()
    value = Field([required()])

    @pass_call
    @pass_new_obj
    def validate_value(self, call, obj, value):
        observation = obj.observation
        observation_type = observation.type
        options = observation.options

        validators = []

        if observation_type == OBSERVATION_TYPE_INTEGER or observation_type == OBSERVATION_TYPE_REAL:
            min_value = options.get('min_value')
            max_value = options.get('max_value')

            if min_value is not None:
                validators.append(min_(min_value))

            if max_value is not None:
                validators.append(max_(max_value))
        elif observation_type == OBSERVATION_TYPE_LOOKUP:
            keys = [x['key'] for x in options['options']]
            validators.append(in_(keys))
        elif observation_type == OBSERVATION_TYPE_STRING:
            min_length_value = options.get('min_length')
            max_length_value = options.get('max_length')

            if min_length_value is not None:
                validators.append(min_length(min_length_value))

            if max_length_value is not None:
                validators.append(max_length(max_length_value))

        value = call.validators(validators, value)

        return value

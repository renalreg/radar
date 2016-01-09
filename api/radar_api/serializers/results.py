from collections import OrderedDict

from radar_api.serializers.data_sources import DataSourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.models.results import Observation, OBSERVATION_TYPE_INTEGER,\
    OBSERVATION_TYPE_REAL, OBSERVATION_TYPE_LOOKUP, OBSERVATION_TYPE_STRING
from radar.serializers.core import Serializer, Empty
from radar.serializers.fields import StringField, IntegerField, FloatField,\
    DateTimeField, UUIDField, ListField
from radar.serializers.models import ReferenceField
from radar.serializers.codes import CodedStringSerializer
from radar.validation.core import ValidationError


class IntegerObservationSerializer(Serializer):
    min_value = IntegerField()
    max_value = IntegerField()
    units = StringField()


class RealObservationSerializer(Serializer):
    min_value = FloatField()
    max_value = FloatField()
    units = StringField()


class OptionSerializer(Serializer):
    key = StringField()
    value = StringField()


class LookupObservationSerializer(Serializer):
    options = ListField(OptionSerializer())


class StringObservationSerializer(Serializer):
    min_length = IntegerField()
    max_length = IntegerField()


class ObservationSerializer(Serializer):
    SERIALIZER_CLASSES = {
        OBSERVATION_TYPE_INTEGER: IntegerObservationSerializer,
        OBSERVATION_TYPE_REAL: RealObservationSerializer,
        OBSERVATION_TYPE_LOOKUP: LookupObservationSerializer,
        OBSERVATION_TYPE_STRING: StringObservationSerializer,
    }

    id = IntegerField()
    type = StringField()
    name = StringField()
    short_name = StringField()

    def to_data(self, observation):
        data = super(ObservationSerializer, self).to_data(observation)

        observation_type = observation.type

        try:
            serializer_class = self.SERIALIZER_CLASSES[observation_type]
        except KeyError:
            raise ValueError('Unknown observation type: %s' % observation_type)

        serializer = serializer_class()
        options_data = serializer.serialize(observation.options)
        data.update(options_data)

        return data

    def to_value(self, data):
        observation = super(ObservationSerializer, self).to_value(data)

        if 'type' in observation:
            observation_type = observation['type']

            try:
                serializer_class = self.SERIALIZER_CLASSES[observation_type]
            except ValueError:
                raise ValidationError({'type': 'Unknown observation type.'})

            serializer = serializer_class()

            try:
                options = serializer.deserialize(data)
            except ValidationError as e:
                raise ValidationError({'options': e.errors})

            observation['options'] = options

        return observation

    def transform_errors(self, errors):
        transformed_errors = super(ObservationSerializer, self).transform_errors(errors)

        if 'options' in errors:
            transformed_errors['options'] = errors['options']

        return transformed_errors


class ObservationReferenceField(ReferenceField):
    model_class = Observation
    serializer_class = ObservationSerializer


class ResultSerializer(PatientSerializerMixin, DataSourceSerializerMixin, MetaSerializerMixin, Serializer):
    id = UUIDField()
    observation = ObservationReferenceField()
    date = DateTimeField()
    created_date = DateTimeField()
    modified_date = DateTimeField()

    def get_value_field(self, observation):
        observation_type = observation.type

        if observation_type == OBSERVATION_TYPE_INTEGER:
            field = IntegerField()
        elif observation_type == OBSERVATION_TYPE_REAL:
            field = FloatField()
        elif observation_type == OBSERVATION_TYPE_LOOKUP:
            options = [(x['key'], x['value']) for x in observation.options['options']]
            options = OrderedDict(options)
            field = CodedStringSerializer(options)
        elif observation_type == OBSERVATION_TYPE_STRING:
            field = StringField()
        else:
            raise ValueError('Unknown observation type: %s' % observation_type)

        return field

    def to_data(self, result):
        data = super(ResultSerializer, self).to_data(result)

        # Serialize the result value
        field = self.get_value_field(result.observation)
        data['value'] = field.serialize(result.value)

        return data

    def to_value(self, data):
        result = super(ResultSerializer, self).to_value(data)

        observation = result.get('observation')

        if observation is not None:
            field = self.get_value_field(observation)
            field.bind('value')

            try:
                value = field.deserialize(data)
            except ValidationError as e:
                raise ValidationError({value: e.errors})

            if value is not Empty:
                result['value'] = value

        return result

    def transform_errors(self, errors):
        transformed_errors = super(ResultSerializer, self).transform_errors(errors)

        if 'value' in errors:
            transformed_errors['value'] = errors['value']

        return transformed_errors

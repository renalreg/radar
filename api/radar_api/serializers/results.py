from collections import OrderedDict

from radar_api.serializers.sources import SourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.models.results import Observation, OBSERVATION_VALUE_TYPE, Result
from radar.serializers.core import Serializer, Empty
from radar.serializers.fields import StringField, IntegerField, FloatField,\
    DateTimeField, UUIDField, ListField, CommaSeparatedField
from radar.serializers.models import ReferenceField
from radar.serializers.fields import LabelledStringField
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
    id = StringField()
    label = StringField()


class LookupObservationSerializer(Serializer):
    options = ListField(OptionSerializer())


class StringObservationSerializer(Serializer):
    min_length = IntegerField()
    max_length = IntegerField()


class ObservationSerializer(Serializer):
    SERIALIZER_CLASSES = {
        OBSERVATION_VALUE_TYPE.INTEGER: IntegerObservationSerializer,
        OBSERVATION_VALUE_TYPE.REAL: RealObservationSerializer,
        OBSERVATION_VALUE_TYPE.ENUM: LookupObservationSerializer,
        OBSERVATION_VALUE_TYPE.STRING: StringObservationSerializer,
    }

    id = IntegerField()
    name = StringField()
    short_name = StringField()
    value_type = StringField()
    sample_type = StringField()

    def to_data(self, observation):
        data = super(ObservationSerializer, self).to_data(observation)

        value_type = observation.value_type

        try:
            serializer_class = self.SERIALIZER_CLASSES[value_type]
        except KeyError:
            raise ValueError('Unknown value type: %s' % value_type)

        serializer = serializer_class()
        properties_data = serializer.serialize(observation.properties)
        data.update(properties_data)

        return data

    def to_value(self, data):
        observation = super(ObservationSerializer, self).to_value(data)

        if 'value_type' in observation:
            value_type = observation['value_type']

            try:
                serializer_class = self.SERIALIZER_CLASSES[value_type]
            except ValueError:
                raise ValidationError({'value_type': 'Unknown value type.'})

            serializer = serializer_class()

            try:
                properties = serializer.deserialize(data)
            except ValidationError as e:
                raise ValidationError({'properties': e.errors})

            observation['properties'] = properties

        return observation

    def transform_errors(self, errors):
        transformed_errors = super(ObservationSerializer, self).transform_errors(errors)

        if 'properties' in errors:
            transformed_errors['properties'] = errors['properties']

        return transformed_errors


class ObservationReferenceField(ReferenceField):
    model_class = Observation
    serializer_class = ObservationSerializer


class ResultSerializer(PatientSerializerMixin, SourceSerializerMixin, MetaSerializerMixin, Serializer):
    id = UUIDField()
    observation = ObservationReferenceField()
    date = DateTimeField()
    created_date = DateTimeField()
    modified_date = DateTimeField()

    def get_value_field(self, observation):
        value_type = observation.value_type

        if value_type == OBSERVATION_VALUE_TYPE.INTEGER:
            field = IntegerField()
        elif value_type == OBSERVATION_VALUE_TYPE.REAL:
            field = FloatField()
        elif value_type == OBSERVATION_VALUE_TYPE.ENUM:
            options = [(x['code'], x['description']) for x in observation.options['options']]
            options = OrderedDict(options)
            field = LabelledStringField(options)
        elif value_type == OBSERVATION_VALUE_TYPE.STRING:
            field = StringField()
        else:
            raise ValueError('Unknown value type: %s' % value_type)

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
                raise ValidationError({'value': e.errors})

            if value is not Empty:
                result['value'] = value

        return result

    def transform_errors(self, errors):
        transformed_errors = super(ResultSerializer, self).transform_errors(errors)

        if 'value' in errors:
            transformed_errors['value'] = errors['value']

        return transformed_errors

    def create(self):
        return Result()

    def update(self, obj, deserialized_data):
        for attr, value in deserialized_data.items():
            setattr(obj, attr, value)

        return obj


class ObservationListRequestSerializer(Serializer):
    type = StringField()
    types = CommaSeparatedField(StringField())


class ResultListRequestSerializer(Serializer):
    observation_id = IntegerField()
    observation_ids = CommaSeparatedField(IntegerField())

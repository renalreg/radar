from collections import OrderedDict

from cornflake import serializers, fields
from cornflake.sqlalchemy_orm import ReferenceField, ModelSerializer
from cornflake.validators import min_, max_, in_, min_length, max_length
from cornflake.exceptions import ValidationError

from radar.models.results import (
    Result,
    Observation,
    OBSERVATION_VALUE_TYPE,
    OBSERVATION_SAMPLE_TYPE,
    OBSERVATION_VALUE_TYPE_NAMES,
    OBSERVATION_SAMPLE_TYPE_NAMES
)
from radar.api.serializers.common import PatientMixin, SourceMixin, MetaMixin


def get_value_field(observation):
    value_type = observation.value_type

    if value_type == OBSERVATION_VALUE_TYPE.INTEGER:
        field = fields.IntegerField()
    elif value_type == OBSERVATION_VALUE_TYPE.REAL:
        field = fields.FloatField()
    elif value_type == OBSERVATION_VALUE_TYPE.ENUM:
        options = [(x['code'], x['description']) for x in observation.properties['options']]
        options = OrderedDict(options)
        field = fields.StringLookupField(options, id_key='code', label_key='description')
    elif value_type == OBSERVATION_VALUE_TYPE.STRING:
        field = fields.StringField()
    else:
        raise ValueError('Unknown value type: %s' % value_type)

    return field


def get_properties_serializer(value_type):
    serializers = {
        OBSERVATION_VALUE_TYPE.INTEGER: IntegerObservationSerializer,
        OBSERVATION_VALUE_TYPE.REAL: RealObservationSerializer,
        OBSERVATION_VALUE_TYPE.ENUM: LookupObservationSerializer,
        OBSERVATION_VALUE_TYPE.STRING: StringObservationSerializer,
    }

    try:
        serializer = serializers[value_type]()
    except KeyError:
        raise ValueError('Unknown value type: %s' % value_type)

    return serializer


class BaseObservationSerializer(serializers.Serializer):
    id = fields.IntegerField()
    name = fields.StringField()
    short_name = fields.StringField()
    value_type = fields.EnumLookupField(OBSERVATION_VALUE_TYPE, OBSERVATION_VALUE_TYPE_NAMES)
    sample_type = fields.EnumLookupField(OBSERVATION_SAMPLE_TYPE, OBSERVATION_SAMPLE_TYPE_NAMES)


class IntegerObservationSerializer(serializers.Serializer):
    min_value = fields.IntegerField(required=False)
    max_value = fields.IntegerField(required=False)
    units = fields.StringField(required=False)


class RealObservationSerializer(serializers.Serializer):
    min_value = fields.FloatField(required=False)
    max_value = fields.FloatField(required=False)
    units = fields.StringField(required=False)


class OptionSerializer(serializers.Serializer):
    code = fields.StringField()
    description = fields.StringField()


class LookupObservationSerializer(serializers.Serializer):
    options = fields.ListField(child=OptionSerializer())


class StringObservationSerializer(serializers.Serializer):
    min_length = fields.IntegerField(required=False)
    max_length = fields.IntegerField(required=False)


class ObservationSerializer(serializers.ProxySerializer):
    def __init__(self, *args, **kwargs):
        super(ObservationSerializer, self).__init__(*args, **kwargs)
        value_type_field = fields.EnumLookupField(OBSERVATION_VALUE_TYPE, OBSERVATION_VALUE_TYPE_NAMES)
        value_type_field.bind(self, 'value_type')
        self.value_type_field = value_type_field

    def get_serializer(self, value_type):
        properties_serializer = get_properties_serializer(value_type)
        serializer = type('CustomObservationSerializer', (BaseObservationSerializer,), {
            'properties': properties_serializer
        })()
        return serializer

    def get_internal_serializer(self, data):
        value_type = self.value_type_field.get_attribute(data)
        serializer = self.get_serializer(value_type)
        return serializer

    def get_external_serializer(self, data):
        value_type_data = self.value_type_field.get_attribute(data)

        try:
            value_type = self.value_type_field.run_validation(value_type_data)
        except ValidationError as e:
            raise ValidationError({self.value_type_field.field_name: e.errors})

        serializer = self.get_serializer(value_type)

        return serializer


class ObservationField(ReferenceField):
    model_class = Observation
    serializer_class = ObservationSerializer


class BaseResultSerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    observation = ObservationField()
    date = fields.DateField()

    class Meta(object):
        model_class = Result

    def validate(self, data):
        data = super(BaseResultSerializer, self).validate(data)

        observation = data['observation']
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

        self.run_validators_on_field(data, self.value, validators)

        return data


class ResultSerializer(serializers.ProxySerializer):
    def __init__(self, *args, **kwargs):
        super(ResultSerializer, self).__init__(*args, **kwargs)
        observation_field = ObservationField()
        observation_field.bind(self, 'observation')
        self.observation_field = observation_field

    def get_serializer(observation):
        field = get_value_field(observation)
        serializer = type('CustomResultSerializer', (BaseResultSerializer,), {
            'value': field
        })()
        return serializer

    def get_internal_serializer(self, data):
        observation = self.observation_field.get_attribute(data)
        serializer = self.get_serializer(observation)
        return serializer

    def get_external_serializer(self, data):
        observation_data = self.observation_field.get_attribute(data)

        try:
            observation = self.observation_field.run_validation(observation_data)
        except ValidationError as e:
            raise ValidationError({self.observation_field.field_name: e.errors})

        serializer = self.get_serializer(observation)

        return serializer


class BaseTinyResultSerializer(PatientMixin, serializers.Serializer):
    id = fields.UUIDField()
    observation = fields.IntegerField(source='observation_id')
    source_type = fields.StringField()
    source_group = fields.IntegerField(source='source_group_id')
    date = fields.DateTimeField()
    created_user = fields.IntegerField(source='created_user_id')
    modified_user = fields.IntegerField(source='modified_user_id')
    created_date = fields.DateTimeField()
    modified_date = fields.DateTimeField()


class TinyResultSerializer(serializers.ProxySerializer):
    def __init__(self, *args, **kwargs):
        super(TinyResultSerializer, self).__init__(*args, **kwargs)
        observation_field = ObservationField()
        observation_field.bind(self, 'observation')
        self.observation_field = observation_field

    def get_serializer(self, observation):
        field = get_value_field(observation)
        serializer = type('CustomTinyResultSerializer', (BaseTinyResultSerializer,), {
            'value': field
        })()
        return serializer

    def get_internal_serializer(self, data):
        observation = self.observation_field.get_attribute(data)
        serializer = self.get_serializer(observation)
        return serializer


class ObservationCountSerializer(serializers.Serializer):
    observation = ObservationSerializer()
    count = fields.IntegerField()

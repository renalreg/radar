from cornflake import serializers, fields
from cornflake.exceptions import ValidationError
from cornflake.sqlalchemy_orm import ReferenceField, ModelSerializer
from cornflake.validators import min_, max_, in_, min_length, max_length

from radar.api.serializers.common import (
    PatientMixin,
    SourceMixin,
    MetaMixin,
    StringLookupField,
    EnumLookupField,
    GroupSerializer
)
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.results import (
    Result,
    Observation,
    OBSERVATION_VALUE_TYPE,
    OBSERVATION_SAMPLE_TYPE,
    OBSERVATION_VALUE_TYPE_NAMES,
    OBSERVATION_SAMPLE_TYPE_NAMES
)


def get_value_field(observation):
    value_type = observation.value_type

    if value_type == OBSERVATION_VALUE_TYPE.INTEGER:
        field = fields.IntegerField()
    elif value_type == OBSERVATION_VALUE_TYPE.REAL:
        field = fields.FloatField()
    elif value_type == OBSERVATION_VALUE_TYPE.ENUM:
        field = StringLookupField(observation.options_dict, key_name='code', value_name='description')
    elif value_type == OBSERVATION_VALUE_TYPE.STRING:
        field = fields.StringField()
    else:
        raise ValueError('Unknown value type: %s' % value_type)

    return field


class OptionSerializer(serializers.Serializer):
    code = fields.StringField()
    description = fields.StringField()


_custom_fields = {
    OBSERVATION_VALUE_TYPE.INTEGER: {
        'min_value': fields.IntegerField(required=False),
        'max_value': fields.IntegerField(required=False),
        'units': fields.StringField(required=False),
    },
    OBSERVATION_VALUE_TYPE.REAL: {
        'min_value': fields.FloatField(required=False),
        'max_value': fields.FloatField(required=False),
        'units': fields.StringField(required=False),
    },
    OBSERVATION_VALUE_TYPE.ENUM: {
        'options': fields.ListField(child=OptionSerializer(), source='code_description_pairs'),
    },
    OBSERVATION_VALUE_TYPE.STRING: {
        'min_length': fields.IntegerField(required=False),
        'max_length': fields.IntegerField(required=False),
    },
}


def get_custom_fields(value_type):
    return _custom_fields.get(value_type, {})


class BaseObservationSerializer(serializers.Serializer):
    id = fields.IntegerField()
    name = fields.StringField()
    short_name = fields.StringField()
    value_type = EnumLookupField(OBSERVATION_VALUE_TYPE, OBSERVATION_VALUE_TYPE_NAMES)
    sample_type = EnumLookupField(OBSERVATION_SAMPLE_TYPE, OBSERVATION_SAMPLE_TYPE_NAMES)
    groups = fields.ListField(child=GroupSerializer())


class ObservationSerializer(serializers.ProxySerializer):
    def __init__(self, *args, **kwargs):
        super(ObservationSerializer, self).__init__(*args, **kwargs)
        value_type_field = EnumLookupField(OBSERVATION_VALUE_TYPE, OBSERVATION_VALUE_TYPE_NAMES)
        value_type_field.bind(self, 'value_type')
        self.value_type_field = value_type_field

    def create_serializer(self, value_type):
        custom_fields = get_custom_fields(value_type)
        serializer = type('CustomObservationSerializer', (BaseObservationSerializer,), custom_fields)()
        return serializer

    def get_serializer(self, data):
        value_type = self.value_type_field.get_attribute(data)
        serializer = self.create_serializer(value_type)
        return serializer

    def get_deserializer(self, data):
        value_type_data = self.value_type_field.get_attribute(data)

        try:
            value_type = self.value_type_field.run_validation(value_type_data)
        except ValidationError as e:
            raise ValidationError({self.value_type_field.field_name: e.errors})

        serializer = self.create_serializer(value_type)

        return serializer


class ObservationField(ReferenceField):
    model_class = Observation
    serializer_class = ObservationSerializer


class BaseResultSerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    observation = ObservationField()

    class Meta(object):
        model_class = Result
        exclude = ['observation_id', '_value']
        validators = [valid_date_for_patient('date')]

    def validate(self, data):
        data = super(BaseResultSerializer, self).validate(data)

        observation = data['observation']
        value_type = observation.value_type

        validators = []

        if value_type == OBSERVATION_VALUE_TYPE.INTEGER or value_type == OBSERVATION_VALUE_TYPE.REAL:
            min_value = observation.min_value
            max_value = observation.max_value

            if min_value is not None:
                validators.append(min_(min_value))

            if max_value is not None:
                validators.append(max_(max_value))
        elif value_type == OBSERVATION_VALUE_TYPE.ENUM:
            codes = observation.option_codes
            validators.append(in_(codes))
        elif value_type == OBSERVATION_VALUE_TYPE.STRING:
            min_length_value = observation.min_length
            max_length_value = observation.max_length

            if min_length_value is not None:
                validators.append(min_length(min_length_value))

            if max_length_value is not None:
                validators.append(max_length(max_length_value))

        self.run_validators_on_field(data, 'value', validators)

        return data


class ResultSerializer(serializers.ProxySerializer):
    def __init__(self, *args, **kwargs):
        super(ResultSerializer, self).__init__(*args, **kwargs)
        observation_field = ObservationField()
        observation_field.bind(self, 'observation')
        self.observation_field = observation_field

    def create_serializer(self, observation):
        field = get_value_field(observation)
        serializer = type('CustomResultSerializer', (BaseResultSerializer,), {
            'value': field
        })()
        return serializer

    def get_serializer(self, data):
        observation = self.observation_field.get_attribute(data)
        serializer = self.create_serializer(observation)
        return serializer

    def get_deserializer(self, data):
        observation_data = self.observation_field.get_attribute(data)

        try:
            observation = self.observation_field.run_validation(observation_data)
        except ValidationError as e:
            raise ValidationError({self.observation_field.field_name: e.errors})

        serializer = self.create_serializer(observation)

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

    def create_serializer(self, observation):
        field = get_value_field(observation)
        serializer = type('CustomTinyResultSerializer', (BaseTinyResultSerializer,), {
            'value': field
        })()
        return serializer

    def get_serializer(self, data):
        observation = self.observation_field.get_attribute(data)
        serializer = self.create_serializer(observation)
        return serializer


class ObservationCountSerializer(serializers.Serializer):
    observation = ObservationSerializer()
    count = fields.IntegerField()

import six

from radar.api.serializers.data_sources import DataSourceSerializerMixin
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.patient_mixins import PatientSerializerMixin
from radar.lib.models import ResultGroupSpec, ResultGroup, RESULT_SPEC_TYPE_INTEGER, RESULT_SPEC_TYPE_FLOAT, \
    RESULT_SPEC_TYPE_CODED_INTEGER, RESULT_SPEC_TYPE_CODED_STRING
from radar.lib.serializers.core import Serializer, Empty, Field
from radar.lib.serializers.fields import StringField, IntegerField, FloatField, DateTimeField, ListField, \
    CommaSeparatedStringField
from radar.lib.serializers.models import ModelSerializer, ReferenceField
from radar.lib.serializers.codes import CodedStringSerializer, CodedIntegerSerializer
from radar.lib.validation.core import ValidationError


class OptionValueField(Field):
    def to_data(self, value):
        if isinstance(value, int):
            return value
        else:
            return six.text_type(value)


class OptionSerializer(Serializer):
    id = OptionValueField()
    label = StringField()


class ResultSpecSerializer(Serializer):
    id = IntegerField()
    code = StringField()
    short_name = StringField()
    name = StringField()
    type = StringField()
    min_value = FloatField()
    max_value = FloatField()
    units = StringField()
    options = ListField(OptionSerializer())


class ResultGroupSpecSerializer(ModelSerializer):
    result_specs = ListField(ResultSpecSerializer(), source='sorted_result_specs')

    class Meta(object):
        model_class = ResultGroupSpec


class ResultGroupSpecReferenceField(ReferenceField):
    model_class = ResultGroupSpec
    serializer_class = ResultGroupSpecSerializer


class ResultField(Field):
    def __init__(self, result_spec, **kwargs):
        super(ResultField, self).__init__(**kwargs)
        self.result_spec = result_spec
        self.field = self.get_field()

    def bind(self, field_name):
        super(ResultField, self).bind(field_name)
        self.field.bind(field_name)

    def get_field(self):
        source = self.result_spec.code

        if self.result_spec.type == RESULT_SPEC_TYPE_INTEGER:
            field = IntegerField(source=source)
        elif self.result_spec.type == RESULT_SPEC_TYPE_FLOAT:
            field = FloatField(source=source)
        elif self.result_spec.type == RESULT_SPEC_TYPE_CODED_STRING:
            field = CodedStringSerializer(self.result_spec.options_as_dict, source=source)
        elif self.result_spec.type == RESULT_SPEC_TYPE_CODED_INTEGER:
            field = CodedIntegerSerializer(self.result_spec.options_as_dict, source=source)
        else:
            field = StringField(source=source)

        return field

    def get_data(self, data):
        return self.field.get_data(data)

    def get_value(self, value):
        return self.field.get_value(value)

    def to_data(self, value):
        return self.field.to_data(value)

    def to_value(self, data):
        return self.field.to_value(data)


class ResultsSerializer(Field):
    def __init__(self, result_group_spec, **kwargs):
        super(ResultsSerializer, self).__init__(**kwargs)
        self.result_group_sec = result_group_spec

    def to_data(self, value):
        results = {}

        for result_spec in self.result_group_sec.result_specs:
            field = ResultField(result_spec)
            field.bind(result_spec.code)

            result_value = field.get_value(value)

            if result_value is Empty:
                result_data = None
            else:
                result_data = field.to_data(result_value)

            results[field.field_name] = result_data

        return results

    def to_value(self, data):
        if data is None:
            return None

        if not isinstance(data, dict):
            raise ValidationError('Expected an object.')

        value = {}
        errors = {}

        for result_spec in self.result_group_sec.result_specs:
            field = ResultField(result_spec)
            field.bind(result_spec.code)
            result_data = field.get_data(data)

            if result_data is Empty:
                continue

            if result_data is None:
                result_value = None
            else:
                try:
                    result_value = field.to_value(result_data)
                except ValidationError as e:
                    errors[field.field_name] = e.errors
                    continue

            value[result_spec.code] = result_value

        if any(errors):
            raise ValidationError(errors)

        return value


class ResultGroupSerializer(PatientSerializerMixin, DataSourceSerializerMixin, MetaSerializerMixin, Serializer):
    id = IntegerField()
    result_group_spec = ResultGroupSpecReferenceField()
    date = DateTimeField()
    created_date = DateTimeField()
    modified_date = DateTimeField()

    @classmethod
    def get_results_serializer(cls, result_group_spec):
        serializer = ResultsSerializer(result_group_spec)
        serializer.bind('results')
        return serializer

    def transform_errors(self, errors):
        transformed_errors = super(ResultGroupSerializer, self).transform_errors(errors)

        if 'results' in errors:
            transformed_errors['results'] = errors['results']

        return transformed_errors

    def to_data(self, value):
        data = super(ResultGroupSerializer, self).to_data(value)
        serializer = self.get_results_serializer(value.result_group_spec)
        data[serializer.field_name] = serializer.to_data(value.results)
        return data

    def to_value(self, data):
        value = super(ResultGroupSerializer, self).to_value(data)

        if 'result_group_spec' in value:
            serializer = self.get_results_serializer(value['result_group_spec'])
            results_data = serializer.get_data(data)

            if results_data is None:
                value[serializer.field_name] = None
            elif results_data is not Empty:
                value[serializer.field_name] = serializer.to_value(results_data)

        return value

    def create(self):
        return ResultGroup()

    def update(self, obj, deserialized_data):
        for attr, value in deserialized_data.items():
            setattr(obj, attr, value)

        return obj


class ResultGroupRequestSerializer(Serializer):
    result_group_codes = CommaSeparatedStringField()
    result_codes = CommaSeparatedStringField()

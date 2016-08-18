import copy

from cornflake import fields
from cornflake import serializers
from cornflake.exceptions import ValidationError
from cornflake.sqlalchemy_orm import ModelSerializer, ReferenceField

from radar.api.serializers.common import MetaMixin, PatientMixin
from radar.marmoset.schema import Schema
from radar.marmoset.registry import Registry
from radar.models import Entry, Form


class FormSerializer(ModelSerializer):
    name = fields.StringField()
    data_ = fields.Field(field_name='data', source='data')

    class Meta(object):
        model_class = Form


class FormField(ReferenceField):
    model_class = Form
    serializer_class = FormSerializer


class DataField(fields.Field):
    def __init__(self, schema, **kwargs):
        super(DataField, self).__init__(**kwargs)
        self.schema = schema

    def __deepcopy__(self, memo):
        kwargs = copy.deepcopy(self._kwargs)
        return self.__class__(self.schema, **kwargs)

    def to_internal_value(self, data):
        data = self.schema.validate(data)
        data = self.schema.format(data)
        return data

    def to_representation(self, data):
        # Data is stored serialized so we need to deserialize it first
        # Note: currently we could just return the stored data here
        # We may want to use a different serialization format for the API and storage
        data = self.schema.parse(data)
        data = self.schema.format(data)
        return data


class BaseEntrySerializer(PatientMixin, MetaMixin, ModelSerializer):
    form = FormField()

    class Meta(object):
        model_class = Entry
        exclude = ['form_id']

    def _save(self, instance, data):
        instance.form = data['form']
        instance.patient = data['patient']

        # Serialize the data before saving (e.g. datetime to string)
        instance.data = self.data.to_representation(data['data'])

        # Metadata
        instance.created_user = data['created_user']
        instance.modified_user = data['modified_user']
        instance.created_date = data['created_date']
        instance.modified_date = data['modified_date']

    def create(self, data):
        instance = Entry()
        self._save(instance, data)
        return instance

    def update(self, instance, data):
        self._save(instance, data)
        return instance


class EntrySerializer(serializers.ProxySerializer):
    def __init__(self, *args, **kwargs):
        super(EntrySerializer, self).__init__(*args, **kwargs)

        # Entry must have a form so we know how to handle the data property/attribute
        self.field = FormField()
        self.field.bind(self, 'form')

    def create_serializer(self, form):
        registry = Registry()
        schema = Schema(registry, form.data)

        data_field = DataField(schema)

        serializer = type('EntrySerializer', (BaseEntrySerializer,), {
            'data': data_field
        })()

        return serializer

    def get_serializer(self, data):
        form = self.field.get_attribute(data)
        serializer = self.create_serializer(form)
        return serializer

    def get_deserializer(self, data):
        form_data = self.field.get_value(data)

        try:
            form = self.field.run_validation(form_data)
        except ValidationError as e:
            raise ValidationError({self.field.field_name: e.errors})

        serializer = self.create_serializer(form)

        return serializer

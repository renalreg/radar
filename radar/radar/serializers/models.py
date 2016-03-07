from sqlalchemy import inspect
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import ColumnProperty
from sqlalchemy.sql import sqltypes
from radar.serializers.core import Serializer, Field
from radar.serializers.fields import StringField, BooleanField, IntegerField, \
    FloatField, DateField, DateTimeField, UUIDField, JSONField


class ModelSerializer(Serializer):
    type_map = {
        sqltypes.String: StringField,
        sqltypes.Integer: IntegerField,
        sqltypes.BigInteger: IntegerField,
        sqltypes.Date: DateField,
        sqltypes.DateTime: DateTimeField,
        sqltypes.Boolean: BooleanField,
        sqltypes.Numeric: FloatField,
        postgresql.INET: StringField,
        postgresql.UUID: UUIDField,
        postgresql.JSONB: JSONField
    }

    class Meta(object):
        model_class = None

    def get_model_class(self):
        return self.Meta.model_class

    def get_model_fields(self):
        """ List of model fields to include (defaults to all) """

        model_fields = getattr(self.Meta, 'fields', None)

        if model_fields:
            model_fields = set(model_fields)

        return model_fields

    def get_model_exclude(self):
        """ List of fields to exclude """

        return set(getattr(self.Meta, 'exclude', []))

    def get_model_read_only(self):
        """ Fields that should be read only (serialized but not deserialized) """

        return set(getattr(self.Meta, 'read_only', []))

    def get_model_write_only(self):
        """ Fields that should be write only (deserialized but not serialized) """

        return set(getattr(self.Meta, 'write_only', []))

    def get_field_class(self, col_type):
        for sql_type, field_type in self.type_map.items():
            if isinstance(col_type, sql_type):
                return field_type

        return None

    def get_fields(self):
        fields = super(ModelSerializer, self).get_fields()

        model_fields = self.get_model_fields()
        model_exclude = self.get_model_exclude()
        model_read_only = self.get_model_read_only()
        model_write_only = self.get_model_write_only()

        props = inspect(self.get_model_class()).attrs

        for prop in props:
            if not isinstance(prop, ColumnProperty):
                continue

            key = prop.key

            # Field explicitly defined
            if key in fields:
                continue

            # Not in field list
            if model_fields and key not in model_fields:
                continue

            # Field excluded
            if key in model_exclude:
                continue

            col = prop.columns[0]
            col_type = col.type

            field_kwargs = {}

            # Read only field
            # Don't allow id column to be updated
            if key in model_read_only or key == 'id':
                field_kwargs['read_only'] = True

            # Write only field
            if key in model_write_only:
                field_kwargs['write_only'] = True

            # Get the field class for this column type
            field_class = self.get_field_class(col_type)

            # This will skip column types we can't handle
            if field_class is not None:
                field = field_class(**field_kwargs)
                field.bind(key)
                fields[key] = field

        return fields

    def create(self):
        model_class = self.get_model_class()
        obj = model_class()
        return obj

    def update(self, obj, deserialized_data):
        for attr, value in deserialized_data.items():
            if hasattr(obj, attr):
                setattr(obj, attr, value)

        return obj


class ReferenceField(Field):
    type_map = {
        sqltypes.String: StringField,
        sqltypes.Integer: IntegerField,
        postgresql.UUID: UUIDField,
    }

    default_error_messages = {
        'not_found': 'Object not found.'
    }

    model_class = None
    model_id = 'id'
    serializer_class = None

    def __init__(self, **kwargs):
        super(ReferenceField, self).__init__(**kwargs)
        self.field = self.get_field()

    def bind(self, field_name):
        super(ReferenceField, self).bind(field_name)
        self.field.bind(field_name)

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer(self):
        serializer_class = self.serializer_class

        if serializer_class is not None:
            serializer = serializer_class(source=self.source)
            serializer.bind(self.field_name)
        else:
            serializer = None

        return serializer

    def get_model_class(self):
        return self.model_class

    def get_model_id(self):
        return self.model_id

    def get_field_class(self):
        prop = getattr(inspect(self.get_model_class()).attrs, self.get_model_id())
        col = prop.columns[0]
        col_type = col.type

        for sql_type, field_type in self.type_map.items():
            if isinstance(col_type, sql_type):
                return field_type

        return StringField

    def get_field(self):
        field_class = self.get_field_class()
        model_id = self.get_model_id()

        return field_class(source=model_id)

    def get_object(self, id):
        model_class = self.get_model_class()
        model_id = self.get_model_id()

        obj = model_class.query.filter(getattr(model_class, model_id) == id).first()

        if obj is None:
            self.fail('not_found')

        return obj

    def get_value(self, value):
        serializer = self.get_serializer()

        if serializer is not None:
            value = serializer.get_value(value)
        else:
            value = super(ReferenceField, self).get_value(value)

            if value is not None:
                value = self.field.get_value(value)

        return value

    def to_value(self, data):
        if isinstance(data, dict):
            model_id = self.get_model_id()
            obj_id = self.field.to_value(data.get(model_id))
        else:
            obj_id = self.field.to_value(data)

        obj = self.get_object(obj_id)

        return obj

    def to_data(self, value):
        serializer = self.get_serializer()

        if serializer is not None:
            return serializer.to_data(value)
        else:
            return self.field.to_data(value)

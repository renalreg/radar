from collections import OrderedDict
import copy
from datetime import datetime, date

import delorean
import six
from sqlalchemy import inspect
from sqlalchemy.orm import ColumnProperty
from sqlalchemy.sql import sqltypes

from radar.lib.validation.core import ValidationError


class Empty(object):
    pass


class Field(object):
    _creation_counter = 0
    default_error_messages = {}

    def __init__(self, read_only=False, write_only=False, default=Empty, source=None, error_messages=None):
        # Keep track of field declaration order
        self._creation_counter = Field._creation_counter
        Field._creation_counter += 1

        self.default = default
        self.read_only = read_only
        self.write_only = write_only
        self.source = source
        self.field_name = None

        messages = {}

        for cls in reversed(self.__class__.__mro__):
            messages.update(getattr(cls, 'default_error_messages', {}))

        if error_messages:
            messages.update(error_messages)

        self.error_messages = messages

    def fail(self, key, **kwargs):
        message = self.error_messages[key]
        message = message.format(**kwargs)
        raise ValidationError(message)

    def bind(self, field_name):
        self.field_name = field_name

        if self.source is None:
            self.source = field_name

    def get_default(self):
        return self.default

    def get_value(self, value):
        if isinstance(value, dict):
            return value.get(self.source, Empty)
        else:
            return getattr(value, self.source, Empty)

    def get_data(self, data):
        return data.get(self.field_name, Empty)

    def to_value(self, data):
        raise NotImplementedError()

    def to_data(self, value):
        raise NotImplementedError()

    def transform_errors(self, errors):
        transformed_errors = {}

        if self.source in errors:
            transformed_errors[self.field_name] = errors[self.source]

        return transformed_errors


class StringField(Field):
    default_error_messages = {
        'invalid': 'A valid string is required.'
    }

    def __init__(self, **kwargs):
        self.trim_whitespace = kwargs.pop('trim_whitespace', True)
        super(StringField, self).__init__(**kwargs)

    def to_value(self, data):
        if data is None:
            return None

        if isinstance(data, dict) or isinstance(data, list) or isinstance(data, bool):
            self.fail('invalid')

        value = six.text_type(data)

        if self.trim_whitespace:
            value = value.strip()

        return value

    def to_data(self, value):
        if value is None:
            return None

        data = six.text_type(value)

        return data


class BooleanField(Field):
    default_error_messages = {
        'invalid': 'A valid boolean is required.'
    }

    TRUE_VALUES = {'t', 'true', 'y', 'yes', '1', 1, True}
    FALSE_VALUES = {'f', 'false', 'n', 'no', '0', 0, False}

    def to_value(self, data):
        if data is None:
            return None

        if hasattr(data, 'lower'):
            data = data.lower()

        # Check for TypeError as list and dict aren't hashable
        try:
            if data in self.TRUE_VALUES:
                return True
            elif data in self.FALSE_VALUES:
                return False
            else:
                self.fail('invalid')
        except TypeError:
            self.fail('invalid')

    def to_data(self, value):
        if value is None:
            return None

        return bool(value)


class IntegerField(Field):
    default_error_messages = {
        'invalid': 'A valid integer is required.'
    }

    def to_value(self, data):
        if data is None:
            return None

        try:
            value = int(data)
            value_f = float(data)

            # No floats
            if value != value_f:
                self.fail('invalid')
        except (ValueError, TypeError):
            self.fail('invalid')

        return value

    def to_data(self, value):
        if value is None:
            return None

        return int(value)


class FloatField(Field):
    default_error_messages = {
        'invalid': 'A valid number is required.'
    }

    def to_value(self, data):
        if data is None:
            return None

        try:
            value = float(data)
        except (ValueError, TypeError):
            self.fail('invalid')

        return value

    def to_data(self, value):
        if value is None:
            return None

        return float(value)


class DateField(Field):
    default_error_messages = {
        'invalid': 'Date has wrong format.',
        'datetime': 'Expected a date but got a datetime.',
    }

    def to_value(self, data):
        if data is None:
            return None

        if isinstance(data, datetime):
            self.fail('datetime')

        if isinstance(data, date):
            return data

        try:
            value = delorean.parse(data).date
        except ValueError:
            self.fail('invalid')

        return value

    def to_data(self, value):
        if value is None:
            return None

        return value.isoformat()


class DateTimeField(Field):
    default_error_messages = {
        'invalid': 'Datetime has wrong format.',
        'date': 'Expected a date but got a datetime.',
    }

    def to_value(self, data):
        if data is None:
            return None

        if isinstance(data, date) and not isinstance(data, datetime):
            self.fail('date')

        if isinstance(data, datetime):
            return data

        try:
            value = delorean.parse(data).datetime
        except ValueError:
            self.fail('invalid')

        return value

    def to_data(self, value):
        return value.isoformat()


class ReferenceField(Field):
    type_map = {
        sqltypes.String: StringField,
        sqltypes.Integer: IntegerField,
    }

    default_error_messages = {
        'not_found': 'Object not found.'
    }

    model_class = None
    model_id = 'id'
    serializer_class = None

    def __init__(self, **kwargs):
        super(ReferenceField, self).__init__(**kwargs)
        self.field = self.get_field(**kwargs)
        self._serializer = None

    def bind(self, field_name):
        super(ReferenceField, self).bind(field_name)
        self.field.bind(field_name)

        serializer = self.get_serializer()

        if serializer is not None:
            serializer.bind(field_name)

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer(self):
        if self._serializer is None:
            serializer_class = self.serializer_class

            if serializer_class is not None:
                self._serializer = serializer_class()

        return self._serializer

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

    def get_field(self, **kwargs):
        field_kwargs = {}

        if 'source' in kwargs:
            field_kwargs['source'] = kwargs['source']

        field_class = self.get_field_class()

        return field_class(**field_kwargs)

    def get_object(self, id):
        obj = self.get_model_class().query.get(id)

        if obj is None:
            self.fail('not_found')

        return obj

    def get_value(self, value):
        serializer = self.get_serializer()

        if serializer is not None:
            return serializer.get_value(value)
        else:
            value = super(ReferenceField, self).get_value(value)
            return self.field.get_value(value)

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


class ListField(Field):
    default_error_messages = {
        'not_a_list': 'Expected a list of items.'
    }

    def __init__(self, field, **kwargs):
        super(ListField, self).__init__(**kwargs)
        self.field = field

    def to_value(self, data):
        if data is None:
            return None

        if not isinstance(data, list):
            self.fail('not_a_list')

        values = []
        errors = {}

        for i, x in enumerate(data):
            try:
                value = self.field.to_value(x)
            except ValidationError as e:
                errors[i] = e.errors
            else:
                values.append(value)

        if any(errors):
            raise ValidationError(errors)

        return values

    def to_data(self, values):
        if values is None:
            return None

        data = []

        for value in values:
            if value is None:
                data.append(None)
            else:
                data.append(self.field.to_data(value))

        return data


class SerializerMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['_declared_fields'] = SerializerMetaclass.get_fields(bases, attrs)
        return super(SerializerMetaclass, cls).__new__(cls, name, bases, attrs)

    @staticmethod
    def get_fields(bases, attrs):
        fields = []

        # Get the fields declared on this class
        for field_name, obj in list(attrs.items()):
            if isinstance(obj, Field):
                fields.append((field_name, attrs.pop(field_name)))

        # Sort the fields in the order they were declared
        fields.sort(key=lambda x: x[1]._creation_counter)

        # Loop in reverse to maintain correct field ordering
        for serializer_class in reversed(bases):
            if hasattr(serializer_class, '_declared_fields'):
                # Copy fields from another serializer
                # Parent serializer's fields go first
                fields = list(serializer_class._declared_fields.items()) + fields
            else:
                # Copy fields from mixins
                mixin_fields = SerializerMetaclass.get_mixin_fields(serializer_class).items()

                # Sort the mixin fields in the order they were declared
                mixin_fields.sort(key=lambda x: x[1]._creation_counter)

                # Add the mixin fields
                fields = mixin_fields + fields

        return OrderedDict(fields)

    @staticmethod
    def get_mixin_fields(field_class):
        fields = {}

        for field_mixin_klass in reversed(field_class.__bases__):
            fields.update(SerializerMetaclass.get_mixin_fields(field_mixin_klass))

        for field_name, obj in field_class.__dict__.items():
            if isinstance(obj, Field):
                fields[field_name] = obj

        return fields


@six.add_metaclass(SerializerMetaclass)
class Serializer(Field):
    def __init__(self, *args, **kwargs):
        super(Serializer, self).__init__(*args, **kwargs)
        self._fields = None

    @property
    def fields(self):
        if self._fields is None:
            self._fields = self.get_fields()

        return self._fields

    @property
    def readable_fields(self):
        return [x for x in self.fields.values() if not x.write_only]

    @property
    def writeable_fields(self):
        return [x for x in self.fields.values() if not x.read_only]

    def get_fields(self):
        # Deep copy the fields before binding them
        fields = copy.deepcopy(self._declared_fields)

        for field_name, field in fields.items():
            field.bind(field_name)

        return fields

    def args_to_value(self, args):
        data = {k: v for k, v in args.items() if len(v.strip()) > 0}
        return self.to_value(data)

    def to_value(self, data):
        errors = {}
        validated_data = OrderedDict()

        if not isinstance(data, dict):
            return Empty

        for field in self.writeable_fields:
            # Get the input data
            field_data = field.get_data(data)

            if field_data is Empty:
                # No value supplied so use default
                value = field.get_default()

                # No default supplied so skip
                if value is Empty:
                    continue
            elif field_data is None:
                value = None
            else:
                # Convert the input data
                try:
                    value = field.to_value(field_data)
                except ValidationError as e:
                    errors[field.field_name] = e.errors
                    continue

                if value is Empty:
                    value = field.get_default()

                    if value is Empty:
                        continue

            validated_data[field.source] = value

        if errors:
            raise ValidationError(errors)

        return validated_data

    def to_data(self, value, **kwargs):
        data = OrderedDict()

        for field in self.readable_fields:
            # Get the instance data
            field_value = field.get_value(value)

            if field_value is Empty:
                continue

            # This saves fields having to handle None themselves
            if field_value is None:
                field_data = None
            else:
                # Convert the data for output
                field_data = field.to_data(field_value)

            data[field.field_name] = field_data

        return data

    def transform_errors(self, errors):
        transformed_errors = {}

        for field in self.fields.values():
            transformed_field_errors = field.transform_errors(errors)
            transformed_errors.update(transformed_field_errors)

        return transformed_errors


class ModelSerializer(Serializer):
    type_map = {
        sqltypes.String: StringField,
        sqltypes.Integer: IntegerField,
        sqltypes.BigInteger: IntegerField,
        sqltypes.Date: DateField,
        sqltypes.DateTime: DateTimeField,
        sqltypes.Boolean: BooleanField,
        sqltypes.Numeric: FloatField,
    }

    class Meta:
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
            if field_class:
                field = field_class(**field_kwargs)
                field.bind(key)
                fields[key] = field

        return fields

    def create(self):
        model_class = self.get_model_class()
        obj = model_class()
        return obj

    def update(self, obj, validated_data):
        for attr, value in validated_data.items():
            setattr(obj, attr, value)

        return obj


class CodedValueSerializer(Serializer):
    def __init__(self, field, items, **kwargs):
        super(CodedValueSerializer, self).__init__(**kwargs)
        self.field = field
        self.items = items

    def transform_errors(self, errors):
        return errors

    def get_fields(self):
        fields = {
            'id': self.field(),
            'value': self.field(read_only=True),
            'label': StringField(read_only=True)
        }

        for field_name, field in fields.items():
            field.bind(field_name)

        return fields

    def to_data(self, value, **kwargs):
        label = self.items[value]
        return super(CodedValueSerializer, self).to_data({
            'id': value,
            'label': label,
        })

    def to_value(self, data):
        if isinstance(data, dict):
            try:
                value = super(CodedValueSerializer, self).to_value(data)
                value = value.get('id')
            except ValidationError as e:
                raise ValidationError(e.errors['id'])
        else:
            value = self.fields['id'].to_value(data)

        return value


class CodedStringSerializer(CodedValueSerializer):
    def __init__(self, items, **kwargs):
        super(CodedStringSerializer, self).__init__(StringField, items, **kwargs)


class CodedIntegerSerializer(CodedValueSerializer):
    def __init__(self, items, **kwargs):
        super(CodedIntegerSerializer, self).__init__(IntegerField, items, **kwargs)

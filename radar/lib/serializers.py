from collections import OrderedDict
import copy
from datetime import datetime, date
import delorean
import six

from sqlalchemy import inspect
from sqlalchemy.orm import ColumnProperty
from sqlalchemy.sql import sqltypes
from radar.models import User, Facility


class Empty(object):
    pass


class ValidationError(Exception):
    def __init__(self, detail):
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = detail


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
        return getattr(value, self.source)

    def get_data(self, data):
        return data.get(self.field_name, Empty)

    def to_value(self, data):
        raise NotImplementedError()

    def to_data(self, value):
        raise NotImplementedError()


class StringField(Field):
    def to_value(self, data):
        value = six.text_type(data)
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

    TRUE_VALUES = {'t', 'T', 'true', 'True', 'TRUE', '1', 1, True}
    FALSE_VALUES = {'f', 'F', 'false', 'False', 'FALSE', '0', 0, False}

    def to_value(self, data):
        if data in self.TRUE_VALUES:
            return True
        elif data in self.FALSE_VALUES:
            return False
        else:
            self.fail('invalid')

    def to_data(self, value):
        if value in self.TRUE_VALUES:
            return True
        elif value in self.FALSE_VALUES:
            return False
        else:
            return bool(value)


class IntegerField(Field):
    default_error_messages = {
        'invalid': 'A valid integer is required.'
    }

    def to_value(self, data):
        try:
            value = int(data)
        except (ValueError, TypeError):
            self.fail('invalid')

        return value

    def to_data(self, value):
        return int(value)


class FloatField(Field):
    default_error_messages = {
        'invalid': 'A valid number is required.'
    }

    def to_value(self, data):
        try:
            value = float(data)
        except (ValueError, TypeError):
            self.fail('invalid')

        return value

    def to_data(self, value):
        return float(value)


class DateField(Field):
    default_error_messages = {
        'invalid': 'Date has wrong format.',
        'datetime': 'Expected a date but got a datetime.',
    }

    def to_value(self, data):
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
        return value.isoformat()


class DateTimeField(Field):
    default_error_messages = {
        'invalid': 'Datetime has wrong format.',
        'date': 'Expected a date but got a datetime.',
    }

    def to_value(self, data):
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


class ListField(Field):
    default_error_messages = {
        'not_a_list': 'Expected a list of items.'
    }

    def __init__(self, item_field):
        super(ListField, self).__init__()
        self.item_field = item_field

    def to_value(self, data):
        if not isinstance(data, list):
            self.fail('not_a_list')

        values = []
        errors = []

        for x in data:
            try:
                value = self.item_field.to_value(x)
            except ValidationError as e:
                errors.append(e.detail)
            else:
                values.append(value)
                errors.append({})

        if any(errors):
            raise ValidationError(errors)

        return values

    def to_data(self, values):
        data = []

        for value in values:
            if value is None:
                data.append(None)
            else:
                data.append(self.item_field.to_data(value))

        return data


class SerializerMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['_declared_fields'] = cls.get_fields(bases, attrs)
        return super(SerializerMetaclass, cls).__new__(cls, name, bases, attrs)

    @classmethod
    def get_fields(cls, bases, attrs):
        fields = []

        # Get the fields declared on this class
        for field_name, obj in list(attrs.items()):
            if isinstance(obj, Field):
                fields.append((field_name, attrs.pop(field_name)))

        # Sort the fields in the order they were declared
        fields.sort(key=lambda x: x[1]._creation_counter)

        # Loop in reverse to maintain correct field ordering
        for base in reversed(bases):
            if hasattr(base, '_declared_fields'):
                # Copy fields from another serializer
                # Parent serializer's fields go first
                fields = list(base._declared_fields.items()) + fields
            else:
                # Copy fields from mixins
                mixin_fields = []

                for field_name, obj in base.__dict__.items():
                    if isinstance(obj, Field):
                        mixin_fields.append((field_name, obj))

                # Sort the mixin fields in the order they were declared
                mixin_fields.sort(key=lambda x: x[1]._creation_counter)

                # Add the mixin fields
                fields = mixin_fields + fields

        return OrderedDict(fields)


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

    def to_value(self, data):
        errors = {}
        validated_data = OrderedDict()

        for field in self.writeable_fields:
            # Get the input data
            field_data = field.get_data(data)

            if field_data is Empty:
                # No value supplied so use default
                value = field.get_default()

                # No default supplied so skip
                if value is Empty:
                    continue
            else:
                # Convert the input data
                try:
                    value = field.to_value(field_data)
                except ValidationError as e:
                    errors[field.field_name] = e.detail
                    continue

            validated_data[field.source] = value

        if errors:
            raise ValidationError(errors)

        return validated_data

    def to_data(self, value):
        data = OrderedDict()

        for field in self.readable_fields:
            # Get the instance data
            field_value = field.get_value(value)

            # This saves fields having to handle None themselves
            if field_value is None:
                field_data = None
            else:
                # Convert the data for output
                field_data = field.to_data(field_value)

            data[field.field_name] = field_data

        return data

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, obj, validated_data):
        raise NotImplementedError()


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
        model = None

    def get_model_class(self):
        return self.Meta.model

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
            if key in model_read_only:
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

    def create(self, validated_data):
        model_class = self.get_model_class()
        obj = model_class(**validated_data)
        return obj

    def update(self, obj, validated_data):
        for attr, value in validated_data.items():
            setattr(obj, attr, value)

        return obj


class EmbeddedUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username']


class EmbeddedFacilitySerializer(ModelSerializer):
    class Meta:
        model = Facility


class CreatedUserMixin(object):
    created_user = EmbeddedUserSerializer(read_only=True)

    def get_model_exclude(self):
        model_exclude = super(CreatedUserMixin, self).get_model_exclude()
        model_exclude.add('created_user_id')
        return model_exclude


class ModifiedUserMixin(object):
    modified_user = EmbeddedUserSerializer(read_only=True)

    def get_model_exclude(self):
        model_exclude = super(ModifiedUserMixin, self).get_model_exclude()
        model_exclude.add('modified_user_id')
        return model_exclude


class MetaSerializerMixin(CreatedUserMixin, ModifiedUserMixin):
    pass


class FacilitySerializerMixin(object):
    facility = EmbeddedFacilitySerializer(read_only=True)

    def get_model_write_only(self):
        model_write_only = super(FacilitySerializerMixin, self).get_model_write_only()
        model_write_only.add('facility_id')
        return model_write_only

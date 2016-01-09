from collections import OrderedDict
import copy

import six

from radar.validation.core import ValidationError


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

    def serialize(self, value):
        if self.source is None:
            field_value = value
        else:
            # Get the instance data
            field_value = self.get_value(value)

        if field_value is Empty:
            field_data = Empty
        elif field_value is None:
            # This saves fields having to handle None themselves
            field_data = None
        else:
            # Convert the data for output
            field_data = self.to_data(field_value)

        return field_data

    def deserialize(self, data):
        if self.field_name is None:
            field_data = data
        else:
            # Get the input data
            field_data = self.get_data(data)

        if field_data is Empty:
            # No value supplied so use default
            field_value = self.get_default()
        elif field_data is None:
            field_value = None
        else:
            # Convert the input data
            field_value = self.to_value(field_data)

            if field_value is Empty:
                field_value = self.get_default()

        return field_value

    def to_value(self, data):
        raise NotImplementedError()

    def to_data(self, value):
        raise NotImplementedError()

    def transform_errors(self, errors):
        return errors


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
    default_error_messages = {
        'not_a_dict': 'Expected an object.'
    }

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
            setattr(self, field_name, field)

        return fields

    def args_to_value(self, args):
        data = {k: v for k, v in args.items() if len(v.strip()) > 0}
        return self.to_value(data)

    def to_value(self, data):
        if data is None:
            return None

        errors = {}
        validated_data = OrderedDict()

        if not isinstance(data, dict):
            self.fail('not_a_dict')

        for field in self.writeable_fields:
            try:
                field_value = field.deserialize(data)
            except ValidationError as e:
                errors[field.field_name] = e.errors
                continue

            if field_value is not Empty:
                validated_data[field.source] = field_value

        if errors:
            raise ValidationError(errors)

        return validated_data

    def to_data(self, value):
        if value is None:
            return None

        data = OrderedDict()

        for field in self.readable_fields:
            field_data = field.serialize(value)

            if field_data is not Empty:
                data[field.field_name] = field_data

        return data

    def transform_errors(self, errors):
        transformed_errors = {}

        # Errors on the serializer
        if '_' in errors:
            transformed_errors['_'] = errors['_']

        for field in self.fields.values():
            field_errors = errors.get(field.source)

            if field_errors is not None:
                transformed_field_errors = field.transform_errors(field_errors)
                transformed_errors[field.source] = transformed_field_errors

        return transformed_errors

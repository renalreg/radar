from collections import OrderedDict
import copy
import six


# error messages
# required


class empty(object):
    pass


class ValidationError(Exception):
    def __init__(self, detail):
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = detail


class BaseSerializer(object):
    default_error_messages = {}

    def __init__(self):
        self.default = empty

    def fail(self, key, **kwargs):
        message = self.default_error_messages[key]
        message = message.format(**kwargs)
        raise ValidationError(message)

    def bind(self, field_name):
        self.field_name = field_name

    def get_default(self):
        return self.default

    def get_value(self, value):
        return getattr(value, self.field_name)

    def get_data(self, data):
        return data.get(self.field_name, empty)

    def to_value(self, data):
        raise NotImplementedError()

    def to_data(self, value):
        raise NotImplementedError()


class StringSerializer(BaseSerializer):
    def to_value(self, data):
        value = six.text_type(data)
        return value

    def to_data(self, value):
        data = six.text_type(value)
        return data


class BooleanSerializer(BaseSerializer):
    default_error_messages = {
        'invalid': 'A valid boolean is required.'
    }

    TRUE_VALUES = set(('t', 'T', 'true', 'True', 'TRUE', '1', 1, True))
    FALSE_VALUES = set(('f', 'F', 'false', 'False', 'FALSE', '0', 0, False))

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


class IntegerSerializer(BaseSerializer):
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


class FloatSerializer(BaseSerializer):
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


class ListSerializer(BaseSerializer):
    default_error_messages = {
        'not_a_list': 'Expected a list of items.'
    }

    def __init__(self, item_field):
        super(ListSerializer, self).__init__()
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
            data.append(self.item_field.to_data(value))

        return data


class SerializerMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['_declared_fields'] = cls.get_fields(bases, attrs)
        return super(SerializerMetaclass, cls).__new__(cls, name, bases, attrs)

    @classmethod
    def get_fields(cls, bases, attrs):
        fields = []

        for field_name, obj in list(attrs.items()):
            if isinstance(obj, BaseSerializer):
                fields.append((field_name, attrs.pop(field_name)))

        for base in reversed(bases):
            if hasattr(base, '_declared_fields'):
                fields = list(base._declared_fields.items()) + fields

        return OrderedDict(fields)


@six.add_metaclass(SerializerMetaclass)
class Serializer(BaseSerializer):
    def __init__(self):
        super(Serializer, self).__init__()
        self._fields = None

    @property
    def fields(self):
        if self._fields is None:
            self._fields = self.get_fields()

        return self._fields

    def get_fields(self):
        fields = copy.deepcopy(self._declared_fields)

        for field_name, field in fields.items():
            field.bind(field_name)

        return fields

    def to_value(self, data):
        errors = {}
        validated_data = {}

        for field in self.fields.values():
            field_data = field.get_data(data)

            if field_data is empty:
                value = field.get_default()

                if value is empty:
                    continue
            else:
                try:
                    value = field.to_value(field_data)
                except ValidationError as e:
                    errors[field.field_name] = e.detail
                    continue

            validated_data[field.field_name] = value

        if errors:
            raise ValidationError(errors)

        return validated_data

    def to_data(self, value):
        data = {}

        for field in self.fields.values():
            field_value = field.get_value(value)
            field_data = field.to_data(field_value)
            data[field.field_name] = field_data

        return data


class ModelSerializer(Serializer):
    class Meta:
        model = None
        fields = None

    def get_fields(self):
        fields = super(ModelSerializer, self).get_fields()

        # TODO
        for x in ['foo', 'bar', 'baz']:
            if x not in fields:
                field = StringSerializer()
                field.bind(x)
                fields[x] = field

        return fields

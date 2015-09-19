from radar.lib.serializers.core import Serializer
from radar.lib.serializers.fields import StringField, IntegerField
from radar.lib.validation.core import ValidationError


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
        if value is None:
            return None

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

from datetime import datetime

from cornflake import fields, serializers
from cornflake.exceptions import ValidationError
from cornflake.validators import upper
import pytz

from radar.api.serializers.validators import _nhs_no, MIN_CHI_NO


def parse_sda_datetime(value):
    value = datetime.strptime('%Y-%m-%d %H:%M:%S', value)
    value = value.replace(tzinfo=pytz.UTC)
    return value


class SDADateTimeField(fields.DateTimeField):
    def parse(self, data):
        try:
            return parse_sda_datetime(data)
        except ValueError:
            return super(SDADateTimeField, self).parse(data)


class CodeDescriptionSerializer(serializers.Serializer):
    code = fields.StringField()
    description = fields.StringField()


class LooseCodeDescriptionSerializer(serializers.Serializer):
    code = fields.StringField(required=False)
    description = fields.StringField(required=False)


class CodeOrDescriptionSerializer(serializers.Serializer):
    code = fields.StringField(required=False)
    description = fields.StringField(required=False)

    def validate(self, data):
        if any((data['code'], data['description'])):
            return data

        raise ValidationError({'code or description': 'At least one is required'})


class _OrganizationSerializer(serializers.Serializer):
    code = fields.StringField(required=False)
    description = fields.StringField(required=False)


class EnteringOrganizationSerializer(serializers.Serializer):
    code = fields.StringField(required=False)
    description = fields.StringField(required=False)
    organization = _OrganizationSerializer(required=False)

    def validate(self, data):
        if data['code'] is None and (data['organization'] is None or data['organization']['code'] is None):
            raise ValidationError({'code': 'This field is required.'})

        return data


class AddressSerializer(serializers.Serializer):
    from_time = SDADateTimeField(required=False)
    to_time = SDADateTimeField(required=False)
    street = fields.StringField(required=False)
    city = CodeOrDescriptionSerializer(required=False)
    state = CodeDescriptionSerializer(required=False)
    country = CodeDescriptionSerializer(required=False)
    zip = CodeOrDescriptionSerializer(required=False)


class ContactInfoSerializer(serializers.Serializer):
    home_phone_number = fields.StringField(required=False)
    work_phone_number = fields.StringField(required=False)
    mobile_phone_number = fields.StringField(required=False)
    email_address = fields.StringField(required=False)


class NameSerializer(serializers.Serializer):
    given_name = fields.StringField(required=False, validators=[upper()])
    family_name = fields.StringField(required=False, validators=[upper()])


class PatientSerializer(serializers.Serializer):
    name = NameSerializer(required=False)
    birth_time = SDADateTimeField(required=False)
    death_time = SDADateTimeField(required=False)
    gender = CodeDescriptionSerializer(required=False)
    ethnic_group = CodeOrDescriptionSerializer(required=False)
    contact_info = ContactInfoSerializer(required=False)


class PatientNumberSerializer(serializers.Serializer):
    number = fields.StringField()
    number_type = fields.StringField()
    organization = CodeDescriptionSerializer()

    def validate(self, value):
        super(PatientNumberSerializer, self).validate(value)
        number_type = value['number_type']
        if number_type in ('NHS', 'CHI', 'HSC'):
            number = value['number']
            try:
                _nhs_no(number, MIN_CHI_NO)
            except ValueError:
                raise ValidationError({'number': 'Not a valid {} number {}'.format(number_type, number)})


class MedicationSerializer(serializers.Serializer):
    external_id = fields.StringField()
    from_time = SDADateTimeField()
    to_time = SDADateTimeField(required=False)
    dose_uom = LooseCodeDescriptionSerializer(required=False)
    order_item = CodeDescriptionSerializer()
    entering_organization = EnteringOrganizationSerializer()
    entered_at = CodeDescriptionSerializer(required=False)


class LabResultItemSerializer(serializers.Serializer):
    observation_time = SDADateTimeField(required=False)
    test_item_code = CodeDescriptionSerializer()
    result_value = fields.StringField()


class ResultSerializer(serializers.Serializer):
    result_items = fields.ListField(child=LabResultItemSerializer())


class LabOrderSerializer(serializers.Serializer):
    external_id = fields.StringField()
    from_time = SDADateTimeField(required=False)
    entering_organization = EnteringOrganizationSerializer()
    result = ResultSerializer()
    entered_at = CodeDescriptionSerializer(required=False)

    def pre_validate(self, data):
        """Populate entering_organization if it is empty from entered_at."""
        if data['entering_organization'] is fields.empty:
            data['entering_organization'] = data['entered_at']
        return super(LabOrderSerializer, self).pre_validate(data)


class ContainerSerializer(serializers.Serializer):
    class PatientSerializer(serializers.Serializer):
        aliases = fields.ListField(child=fields.Field(), required=False)
        addresses = fields.ListField(child=fields.Field(), required=False)
        patient_numbers = fields.ListField(child=PatientNumberSerializer())

    patient = PatientSerializer()
    lab_orders = fields.ListField(child=fields.Field(), required=False)
    medications = fields.ListField(child=fields.Field(), required=False)

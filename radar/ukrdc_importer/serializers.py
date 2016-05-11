from datetime import datetime

import pytz

from cornflake import fields, serializers


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


class AddressSerializer(serializers.Serializer):
    from_time = SDADateTimeField(required=False)
    to_time = SDADateTimeField(required=False)
    street = fields.StringField(required=False)
    city = CodeDescriptionSerializer(required=False)
    state = CodeDescriptionSerializer(required=False)
    country = CodeDescriptionSerializer(required=False)
    zip = CodeDescriptionSerializer(required=False)


class ContactInfoSerializer(serializers.Serializer):
    home_phone_number = fields.StringField(required=False)
    work_phone_number = fields.StringField(required=False)
    mobile_phone_number = fields.StringField(required=False)
    email_address = fields.StringField(required=False)


class NameSerializer(serializers.Serializer):
    given_name = fields.StringField(required=False)
    family_name = fields.StringField(required=False)


class PatientSerializer(serializers.Serializer):
    name = NameSerializer(required=False)
    birth_time = SDADateTimeField(required=False)
    death_time = SDADateTimeField(required=False)
    gender = CodeDescriptionSerializer(required=False)
    ethnic_group = CodeDescriptionSerializer(required=False)
    contact_info = ContactInfoSerializer(required=False)


class PatientNumberSerializer(serializers.Serializer):
    number = fields.StringField()
    number_type = fields.StringField()
    organization = CodeDescriptionSerializer()


class DrugProductSerializer(serializers.Serializer):
    product_name = fields.StringField()


class MedicationSerializer(serializers.Serializer):
    external_id = fields.StringField()
    from_time = SDADateTimeField()
    to_time = SDADateTimeField(required=False)
    dose_u_o_m = CodeDescriptionSerializer()
    drug_product = DrugProductSerializer()
    entering_organization = CodeDescriptionSerializer()


class LabResultItemSerializer(serializers.Serializer):
    observation_time = SDADateTimeField()
    test_item_code = CodeDescriptionSerializer()
    result_value = fields.FloatField()


class ResultSerializer(serializers.Serializer):
    result_items = fields.ListField(child=LabResultItemSerializer())


class LabOrderSerializer(serializers.Serializer):
    external_id = fields.StringField()
    from_time = SDADateTimeField(required=False)
    entering_organization = CodeDescriptionSerializer()


class ContainerSerializer(serializers.Serializer):
    class PatientSerializer(serializers.Serializer):
        patient_numbers = fields.ListField(child=PatientNumberSerializer())

    patient = PatientSerializer()
    lab_orders = fields.ListField(child=fields.Field(), required=False)
    medications = fields.ListField(child=fields.Field(), required=False)

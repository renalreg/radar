from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, DateTimeField, ListField, FloatField


class CodeSerializer(Serializer):
    code = StringField()
    description = StringField()


class OrganizationCodeSerializer(CodeSerializer):
    pass


class GenderCodeSerializer(CodeSerializer):
    pass


class DrugProductCodeSerializer(CodeSerializer):
    product_name = StringField()


class RouteCodeSerializer(CodeSerializer):
    pass


class FrequencyCodeSerializer(CodeSerializer):
    pass


class OrderCodeSerializer(CodeSerializer):
    pass


class LabTestItemCodeSerializer(CodeSerializer):
    pass


class ObservationCodeSerializer(CodeSerializer):
    pass


class UserCodeSerializer(CodeSerializer):
    pass


class NameSerializer(Serializer):
    given_name = StringField()
    family_name = StringField()


class PatientNumberSerializer(Serializer):
    entered_at = OrganizationCodeSerializer()
    number = StringField()
    organization = OrganizationCodeSerializer()


class PatientSerializer(Serializer):
    external_id = StringField()
    entered_at = OrganizationCodeSerializer()
    name = NameSerializer()
    birth_time = DateTimeField()
    gender = GenderCodeSerializer()
    patient_numbers = ListField(PatientNumberSerializer())


class MedicationSerializer(Serializer):
    external_id = StringField()
    entered_at = OrganizationCodeSerializer()
    from_time = DateTimeField()
    to_time = DateTimeField()
    drug_product = DrugProductCodeSerializer()
    route = RouteCodeSerializer()
    frequency = FrequencyCodeSerializer()
    dose_quantity = FloatField()
    dose_u_o_m = StringField()


class LabResultItem(Serializer):
    test_item_code = LabTestItemCodeSerializer()
    result_value = StringField()


class ResultSerializer(Serializer):
    result_items = ListField()


class LabOrderSerializer(Serializer):
    external_id = StringField()
    entered_at = OrganizationCodeSerializer()
    from_time = DateTimeField()
    order_item = OrderCodeSerializer()


class ObservationSerializer(Serializer):
    external_id = StringField()
    entered_at = OrganizationCodeSerializer()
    observation_code = ObservationCodeSerializer()
    observation_value = StringField()
    observation_time = DateTimeField()


class ProgramMembershipSerializer(Serializer):
    entered_by = UserCodeSerializer()
    entered_at = OrganizationCodeSerializer()
    entered_on = DateTimeField()
    program_name = StringField()
    from_time = DateTimeField()


class ContainerSerializer(Serializer):
    patient = PatientSerializer()
    medications = ListField(MedicationSerializer())
    lab_orders = ListField(LabOrderSerializer())
    observations = ListField(ObservationSerializer())
    program_memberships = ListField(ProgramMembershipSerializer())

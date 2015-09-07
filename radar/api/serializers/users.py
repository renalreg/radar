from radar.api.serializers.patients import UnitLookupField, DiseaseGroupLookupField
from radar.lib.serializers import Serializer, IntegerField, StringField, MetaSerializerMixin, ModelSerializer, ListField, \
    BooleanField
from radar.models import UnitUser, Unit, Facility, User


class FacilitySerializer(ModelSerializer):
    class Meta:
        model_class = Facility


class UnitSerializer(ModelSerializer):
    facilities = ListField(field=FacilitySerializer())

    class Meta:
        model_class = Unit


class UnitUserSerializer(MetaSerializerMixin, ModelSerializer):
    has_view_demographics_permission = BooleanField()
    has_view_patient_permission = BooleanField()
    has_edit_patient_permission = BooleanField()
    has_view_user_permission = BooleanField()
    has_edit_user_membership_permission = BooleanField()
    has_recruit_patient_permission = BooleanField()
    unit = UnitSerializer()

    class Meta:
        model_class = UnitUser
        exclude = ('unit_id',)


class UserSerializer(MetaSerializerMixin, ModelSerializer):
    units = ListField(field=UnitUserSerializer(), source='unit_users')

    class Meta:
        model_class = User
        fields = ('id', 'is_admin', 'username', 'email')


class UserListRequestSerializer(Serializer):
    id = IntegerField()
    username = StringField()
    email = StringField()
    first_name = StringField()
    last_name = StringField()
    unit_id = UnitLookupField(write_only=True)
    disease_group_id = DiseaseGroupLookupField(write_only=True)

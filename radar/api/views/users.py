from radar.lib.serializers import MetaSerializerMixin, ModelSerializer, ListField, BooleanField
from radar.lib.views import ListCreateApiView, RetrieveUpdateDestroyAPIView
from radar.models import User, UnitUser, Unit, Facility


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


class UserList(ListCreateApiView):
    serializer_class = UserSerializer
    model_class = User


class UserDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    model_class = User

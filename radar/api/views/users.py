from flask import request
from flask_login import current_user
from radar.api.views.patients import UnitLookupField, DiseaseGroupLookupField
from radar.lib.permissions import IsAuthenticated
from radar.lib.serializers import MetaSerializerMixin, ModelSerializer, ListField, BooleanField, Serializer, \
    IntegerField, StringField
from radar.lib.user_search import UserQueryBuilder
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


class UserListRequestSerializer(Serializer):
    id = IntegerField()
    username = StringField()
    email = StringField()
    first_name = StringField()
    last_name = StringField()
    unit_id = UnitLookupField(write_only=True)
    disease_group_id = DiseaseGroupLookupField(write_only=True)


class UserList(ListCreateApiView):
    serializer_class = UserSerializer
    model_class = User
    sort_fields = ('id', 'username', 'email', 'first_name', 'last_name')
    permission_classes = [IsAuthenticated]

    def get_query(self):
        serializer = UserListRequestSerializer()
        args = serializer.args_to_value(request.args)

        builder = UserQueryBuilder(current_user)

        if 'id' in args:
            builder.user_id(args['id'])

        if 'username' in args:
            builder.username(args['username'])

        if 'email' in args:
            builder.email(args['email'])

        if 'first_name' in args:
            builder.first_name(args['first_name'])

        if 'last_name' in args:
            builder.last_name(args['last_name'])

        if 'disease_group' in args:
            builder.disease_group(args['disease_group'])

        if 'unit' in args:
            builder.unit(args['unit'])

        query = builder.build()

        return query


class UserDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    model_class = User

from radar.lib.serializers import MetaSerializerMixin, ModelSerializer, ListField
from radar.lib.views import ListCreateApiView, RetrieveUpdateDestroyAPIView
from radar.models import User, UnitUser


class UnitUserSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = UnitUser


class UserSerializer(MetaSerializerMixin, ModelSerializer):
    units = ListField(field=UnitUserSerializer(), source='unit_users')

    class Meta:
        model_class = User
        fields = ('id', 'is_admin', 'username', 'email')


class UserList(ListCreateApiView):
    serializer_class = UserSerializer

    def get_query(self):
        return User.query


class UserDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_query(self):
        return User.query

from radar.lib.models import User
from radar.lib.serializers import ModelSerializer


class BasicUserSerializer(ModelSerializer):
    class Meta(object):
        model_class = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username']


class CreatedUserMixin(object):
    created_user = BasicUserSerializer(read_only=True)

    def get_model_exclude(self):
        model_exclude = super(CreatedUserMixin, self).get_model_exclude()
        model_exclude.add('created_user_id')
        return model_exclude


class ModifiedUserMixin(object):
    modified_user = BasicUserSerializer(read_only=True)

    def get_model_exclude(self):
        model_exclude = super(ModifiedUserMixin, self).get_model_exclude()
        model_exclude.add('modified_user_id')
        return model_exclude


class MetaSerializerMixin(CreatedUserMixin, ModifiedUserMixin):
    pass

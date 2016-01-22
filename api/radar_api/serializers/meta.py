from radar.models.users import User
from radar.serializers.fields import StringField, IntegerField, DateTimeField
from radar.serializers.models import ModelSerializer


class TinyUserSerializer(ModelSerializer):
    id = IntegerField()
    username = StringField()
    email = StringField()
    first_name = StringField()
    last_name = StringField()

    class Meta:
        model_class = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name'
        )


class CreatedUserMixin(object):
    created_user = TinyUserSerializer(read_only=True)

    def get_model_exclude(self):
        model_exclude = super(CreatedUserMixin, self).get_model_exclude()
        model_exclude.add('created_user_id')
        return model_exclude


class ModifiedUserMixin(object):
    modified_user = TinyUserSerializer(read_only=True)

    def get_model_exclude(self):
        model_exclude = super(ModifiedUserMixin, self).get_model_exclude()
        model_exclude.add('modified_user_id')
        return model_exclude


class CreatedDateMixin(object):
    created_date = DateTimeField(read_only=False)


class ModifiedDateMixin(object):
    modified_date = DateTimeField(read_only=False)


class MetaSerializerMixin(CreatedUserMixin, ModifiedUserMixin, CreatedDateMixin, ModifiedDateMixin):
    pass

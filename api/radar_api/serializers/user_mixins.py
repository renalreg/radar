from radar_api.serializers.user_fields import UserReferenceField


class UserSerializerMixin(object):
    user = UserReferenceField()

    def get_model_exclude(self):
        attrs = super(UserSerializerMixin, self).get_model_exclude()
        attrs.add('user_id')
        return attrs

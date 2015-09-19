from radar.lib.models import User
from radar.lib.serializers.models import ReferenceField


class UserReferenceField(ReferenceField):
    model_class = User


class UserSerializerMixin(object):
    user = UserReferenceField()

    def get_model_exclude(self):
        attrs = super(UserSerializerMixin, self).get_model_exclude()
        attrs.add('user_id')
        return attrs

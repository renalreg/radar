from radar.lib.models import User
from radar.lib.serializers.models import ReferenceField


class UserReferenceField(ReferenceField):
    model_class = User

from radar.models import User
from radar.serializers.models import ReferenceField


class UserReferenceField(ReferenceField):
    model_class = User

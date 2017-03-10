from cornflake.sqlalchemy_orm import ModelSerializer, ReferenceField
from radar.models.nationalities import Nationality


class NationalitySerializer(ModelSerializer):
    class Meta(object):
        model_class = Nationality


class NationalityField(ReferenceField):
    model_class = Nationality
    serializer_class = NationalitySerializer

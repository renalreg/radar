from cornflake.sqlalchemy_orm import ModelSerializer, ReferenceField
from radar.models.demographics import Ethnicity, Nationality


class NationalitySerializer(ModelSerializer):
    class Meta(object):
        model_class = Nationality


class NationalityField(ReferenceField):
    model_class = Nationality
    serializer_class = NationalitySerializer


class EthnicitySerializer(ModelSerializer):
    class Meta(object):
        model_class = Ethnicity


class EthnicityField(ReferenceField):
    model_class = Ethnicity
    serializer_class = EthnicitySerializer


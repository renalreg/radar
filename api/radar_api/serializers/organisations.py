from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, ListField, BooleanField
from radar.serializers.models import ModelSerializer, ReferenceField
from radar.models import DataSource, Organisation


class TinyOrganisationSerializer(ModelSerializer):
    class Meta(object):
        model_class = Organisation
        fields = ['id', 'code', 'type', 'name']


class DataSourceSerializer(ModelSerializer):
    organisation = TinyOrganisationSerializer()

    class Meta(object):
        model_class = DataSource


class OrganisationSerializer(ModelSerializer):
    data_sources = ListField(field=DataSourceSerializer())

    class Meta(object):
        model_class = Organisation


class OrganisationReferenceField(ReferenceField):
    model_class = Organisation
    serializer_class = OrganisationSerializer


class TinyOrganisationReferenceField(ReferenceField):
    model_class = Organisation
    serializer_class = TinyOrganisationSerializer


class OrganisationRequestSerializer(Serializer):
    type = StringField()
    recruitment = BooleanField()

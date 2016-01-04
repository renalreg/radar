from radar_api.serializers.meta import MetaSerializerMixin
from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, ListField, BooleanField
from radar.serializers.models import ModelSerializer, ReferenceField
from radar.models import DataSource, Organisation


class BasicOrganisationSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = Organisation
        exclude = ['organisation_id']


class DataSourceSerializer(ModelSerializer):
    organisation = BasicOrganisationSerializer()

    class Meta(object):
        model_class = DataSource


class OrganisationSerializer(ModelSerializer):
    data_sources = ListField(field=DataSourceSerializer())

    class Meta(object):
        model_class = Organisation


class OrganisationReferenceField(ReferenceField):
    model_class = Organisation
    serializer_class = OrganisationSerializer


class OrganisationRequestSerializer(Serializer):
    type = StringField()
    recruitment = BooleanField()

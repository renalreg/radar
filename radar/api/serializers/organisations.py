from radar.api.serializers.meta import MetaSerializerMixin
from radar.lib.serializers import ModelSerializer, ListField, ReferenceField
from radar.lib.models import DataSource, Organisation


class BasicOrganisationSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = Organisation
        exclude = ['organisation_id']


class OrganisationReferenceField(ReferenceField):
    model_class = Organisation
    serializer_class = BasicOrganisationSerializer


class DataSourceSerializer(ModelSerializer):
    organisation = BasicOrganisationSerializer()

    class Meta(object):
        model_class = DataSource


class OrganisationSerializer(ModelSerializer):
    data_sources = ListField(field=DataSourceSerializer())

    class Meta(object):
        model_class = Organisation

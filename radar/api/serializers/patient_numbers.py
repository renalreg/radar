from radar.api.serializers.data_sources import DataSourceSerializerMixin
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.organisations import OrganisationReferenceField
from radar.api.serializers.patient_mixins import PatientSerializerMixin
from radar.lib.serializers.models import ModelSerializer
from radar.lib.models import PatientNumber


class PatientNumberSerializer(PatientSerializerMixin, DataSourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    organisation = OrganisationReferenceField()

    class Meta(object):
        model_class = PatientNumber
        exclude = ['organisation_id']

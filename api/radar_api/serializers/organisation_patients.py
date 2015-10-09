from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.organisations import OrganisationReferenceField
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.models import OrganisationPatient
from radar.serializers.models import ModelSerializer


class OrganisationPatientSerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    organisation = OrganisationReferenceField()

    class Meta(object):
        model_class = OrganisationPatient
        exclude = ['organisation_id']

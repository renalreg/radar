from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.organisations import OrganisationReferenceField
from radar.api.serializers.patient_mixins import PatientSerializerMixin
from radar.lib.models import OrganisationPatient
from radar.lib.serializers.models import ModelSerializer


class OrganisationPatientSerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    organisation = OrganisationReferenceField()

    class Meta(object):
        model_class = OrganisationPatient
        exclude = ['organisation_id']

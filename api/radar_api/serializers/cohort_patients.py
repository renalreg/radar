from radar_api.serializers.cohorts import CohortReferenceField
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.organisations import OrganisationReferenceField
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.models import CohortPatient
from radar.serializers.models import ModelSerializer


class CohortPatientSerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    cohort = CohortReferenceField()
    recruited_organisation = OrganisationReferenceField()

    class Meta(object):
        model_class = CohortPatient
        exclude = ['cohort_id']

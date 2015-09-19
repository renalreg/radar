from radar.api.serializers.cohorts import CohortReferenceField
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.organisations import OrganisationReferenceField
from radar.api.serializers.patient_mixins import PatientSerializerMixin
from radar.lib.models import CohortPatient
from radar.lib.serializers.models import ModelSerializer


class CohortPatientSerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    cohort = CohortReferenceField()
    recruiting_organisation = OrganisationReferenceField()

    class Meta(object):
        model_class = CohortPatient
        exclude = ['cohort_id']

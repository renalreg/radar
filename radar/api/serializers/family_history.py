from radar.api.serializers.cohorts import CohortSerializerMixin
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.patient_mixins import PatientSerializerMixin
from radar.lib.models.family_history import FamilyHistory
from radar.lib.serializers import ModelSerializer


class FamilyHistorySerializer(PatientSerializerMixin, CohortSerializerMixin, MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = FamilyHistory

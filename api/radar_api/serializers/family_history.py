from radar_api.serializers.cohorts import CohortSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.models.family_history import FamilyHistory
from radar.serializers.models import ModelSerializer


class FamilyHistorySerializer(PatientSerializerMixin, CohortSerializerMixin, MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = FamilyHistory

from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.patients import PatientSerializerMixin
from radar.lib.models.family_history import FamilyHistory
from radar.lib.serializers import ModelSerializer


class FamilyHistorySerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = FamilyHistory

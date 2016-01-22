from radar_api.serializers.meta import MetaSerializerMixin
from radar.serializers.models import ModelSerializer
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.models.salt_wasting import SaltWastingClinicalFeatures


class SaltWastingClinicalFeaturesSerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = SaltWastingClinicalFeatures

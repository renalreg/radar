from radar.api.serializers.meta import MetaSerializerMixin
from radar.lib.serializers import ModelSerializer
from radar.lib.models import SaltWastingClinicalFeatures


class SaltWastingClinicalFeaturesSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = SaltWastingClinicalFeatures

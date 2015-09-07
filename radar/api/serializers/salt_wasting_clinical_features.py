from radar.lib.serializers import ModelSerializer, MetaSerializerMixin
from radar.models import SaltWastingClinicalFeatures


class SaltWastingClinicalFeaturesSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = SaltWastingClinicalFeatures

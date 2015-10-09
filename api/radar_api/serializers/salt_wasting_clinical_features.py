from radar_api.serializers.meta import MetaSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.models import SaltWastingClinicalFeatures


class SaltWastingClinicalFeaturesSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = SaltWastingClinicalFeatures

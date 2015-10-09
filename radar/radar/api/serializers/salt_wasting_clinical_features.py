from radar.api.serializers.meta import MetaSerializerMixin
from radar.lib.serializers.models import ModelSerializer
from radar.lib.models import SaltWastingClinicalFeatures


class SaltWastingClinicalFeaturesSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = SaltWastingClinicalFeatures

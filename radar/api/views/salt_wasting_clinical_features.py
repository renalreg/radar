from radar.lib.serializers import MetaSerializerMixin, ModelSerializer
from radar.lib.views import PatientDataDetail, PatientDataList
from radar.models import SaltWastingClinicalFeatures


class SaltWastingClinicalFeaturesSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = SaltWastingClinicalFeatures


class SaltWastingClinicalFeaturesList(PatientDataList):
    serializer_class = SaltWastingClinicalFeaturesSerializer
    model_class = SaltWastingClinicalFeatures


class SaltWastingClinicalFeaturesDetail(PatientDataDetail):
    serializer_class = SaltWastingClinicalFeaturesSerializer
    model_class = SaltWastingClinicalFeatures

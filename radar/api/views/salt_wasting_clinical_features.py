from radar.lib.serializers import MetaSerializerMixin, ModelSerializer
from radar.lib.views import PatientDataDetail, PatientDataList
from radar.models import SaltWastingClinicalFeatures


class SaltWastingClinicalFeaturesSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta:
        model = SaltWastingClinicalFeatures


class SaltWastingClinicalFeaturesList(PatientDataList):
    serializer_class = SaltWastingClinicalFeaturesSerializer

    def get_query(self):
        return SaltWastingClinicalFeatures.query


class SaltWastingClinicalFeaturesDetail(PatientDataDetail):
    serializer_class = SaltWastingClinicalFeaturesSerializer

    def get_query(self):
        return SaltWastingClinicalFeatures.query

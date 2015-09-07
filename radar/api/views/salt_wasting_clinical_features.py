from radar.api.serializers.salt_wasting_clinical_features import SaltWastingClinicalFeaturesSerializer
from radar.lib.views import PatientDataDetail, PatientDataList
from radar.models import SaltWastingClinicalFeatures


class SaltWastingClinicalFeaturesList(PatientDataList):
    serializer_class = SaltWastingClinicalFeaturesSerializer
    model_class = SaltWastingClinicalFeatures


class SaltWastingClinicalFeaturesDetail(PatientDataDetail):
    serializer_class = SaltWastingClinicalFeaturesSerializer
    model_class = SaltWastingClinicalFeatures

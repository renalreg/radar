from radar_api.serializers.salt_wasting_clinical_features import SaltWastingClinicalFeaturesSerializer
from radar.models import SaltWastingClinicalFeatures
from radar.validation.salt_wasting import SaltWastingClinicalFeaturesValidation
from radar.views.patients import PatientObjectListView, PatientObjectDetailView


class SaltWastingClinicalFeaturesListView(PatientObjectListView):
    serializer_class = SaltWastingClinicalFeaturesSerializer
    model_class = SaltWastingClinicalFeatures
    validation_class = SaltWastingClinicalFeaturesValidation


class SaltWastingClinicalFeaturesDetailView(PatientObjectDetailView):
    serializer_class = SaltWastingClinicalFeaturesSerializer
    model_class = SaltWastingClinicalFeatures
    validation_class = SaltWastingClinicalFeaturesValidation

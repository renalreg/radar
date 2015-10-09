from radar.api.serializers.salt_wasting_clinical_features import SaltWastingClinicalFeaturesSerializer
from radar.lib.models import SaltWastingClinicalFeatures
from radar.lib.validation.salt_wasting import SaltWastingClinicalFeaturesValidation
from radar.lib.views.patients import PatientObjectListView, PatientObjectDetailView


class SaltWastingClinicalFeaturesListView(PatientObjectListView):
    serializer_class = SaltWastingClinicalFeaturesSerializer
    model_class = SaltWastingClinicalFeatures
    validation_class = SaltWastingClinicalFeaturesValidation


class SaltWastingClinicalFeaturesDetailView(PatientObjectDetailView):
    serializer_class = SaltWastingClinicalFeaturesSerializer
    model_class = SaltWastingClinicalFeatures
    validation_class = SaltWastingClinicalFeaturesValidation

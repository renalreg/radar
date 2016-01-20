from radar_api.serializers.salt_wasting_clinical_features import SaltWastingClinicalFeaturesSerializer
from radar.models.salt_wasting import SaltWastingClinicalFeatures
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


def register_views(app):
    app.add_url_rule(
        '/salt-wasting-clinical-features',
        view_func=SaltWastingClinicalFeaturesListView.as_view('salt_wasting_clinical_features_list')
    )
    app.add_url_rule(
        '/salt-wasting-clinical-features/<id>',
        view_func=SaltWastingClinicalFeaturesDetailView.as_view('salt_wasting_clinical_features_detail')
    )

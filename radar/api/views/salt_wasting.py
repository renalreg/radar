from radar.api.serializers.salt_wasting import SaltWastingClinicalFeaturesSerializer
from radar.api.views.common import (
    PatientObjectListView,
    PatientObjectDetailView
)
from radar.models.salt_wasting import SaltWastingClinicalFeatures


class SaltWastingClinicalFeaturesListView(PatientObjectListView):
    serializer_class = SaltWastingClinicalFeaturesSerializer
    model_class = SaltWastingClinicalFeatures


class SaltWastingClinicalFeaturesDetailView(PatientObjectDetailView):
    serializer_class = SaltWastingClinicalFeaturesSerializer
    model_class = SaltWastingClinicalFeatures


def register_views(app):
    app.add_url_rule(
        '/salt-wasting-clinical-features',
        view_func=SaltWastingClinicalFeaturesListView.as_view('salt_wasting_clinical_features_list')
    )
    app.add_url_rule(
        '/salt-wasting-clinical-features/<id>',
        view_func=SaltWastingClinicalFeaturesDetailView.as_view('salt_wasting_clinical_features_detail')
    )

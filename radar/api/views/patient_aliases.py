from radar.api.serializers.patient_aliases import PatientAliasSerializer
from radar.lib.models import PatientAlias
from radar.lib.validation.patient_aliases import PatientAliasValidation
from radar.lib.views.data_sources import RadarObjectViewMixin
from radar.lib.views.patients import PatientObjectListView, PatientObjectDetailView


class PatientAliasListView(RadarObjectViewMixin, PatientObjectListView):
    serializer_class = PatientAliasSerializer
    model_class = PatientAlias
    validation_class = PatientAliasValidation


class PatientAliasDetailView(RadarObjectViewMixin, PatientObjectDetailView):
    serializer_class = PatientAliasSerializer
    model_class = PatientAlias
    validation_class = PatientAliasValidation

from radar_api.serializers.patient_aliases import PatientAliasSerializer
from radar.models import PatientAlias
from radar.validation.patient_aliases import PatientAliasValidation
from radar.views.data_sources import RadarObjectViewMixin
from radar.views.patients import PatientObjectListView, PatientObjectDetailView, DemographicsViewMixin


class PatientAliasListView(RadarObjectViewMixin, DemographicsViewMixin, PatientObjectListView):
    serializer_class = PatientAliasSerializer
    model_class = PatientAlias
    validation_class = PatientAliasValidation


class PatientAliasDetailView(RadarObjectViewMixin, DemographicsViewMixin, PatientObjectDetailView):
    serializer_class = PatientAliasSerializer
    model_class = PatientAlias
    validation_class = PatientAliasValidation

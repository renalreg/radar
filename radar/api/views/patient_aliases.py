from radar.api.serializers.patient_aliases import PatientAliasSerializer
from radar.lib.models import PatientAlias
from radar.lib.validation.patient_aliases import PatientAliasValidation
from radar.lib.views.data_sources import DataSourceObjectViewMixin
from radar.lib.views.patients import PatientObjectListView, PatientObjectDetailView


class PatientAliasListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = PatientAliasSerializer
    model_class = PatientAlias
    validation_class = PatientAliasValidation


class PatientAliasDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = PatientAliasSerializer
    model_class = PatientAlias
    validation_class = PatientAliasValidation

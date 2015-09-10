from radar.api.serializers.patient_aliases import PatientAliasSerializer
from radar.lib.views import PatientDataList, FacilityDataMixin, PatientDataDetail
from radar.models import PatientAlias


class PatientAliasList(FacilityDataMixin, PatientDataList):
    serializer_class = PatientAliasSerializer
    model_class = PatientAlias


class PatientAliasDetail(FacilityDataMixin, PatientDataDetail):
    serializer_class = PatientAliasSerializer
    model_class = PatientAlias

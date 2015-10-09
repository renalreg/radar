from radar_api.serializers.organisation_patients import OrganisationPatientSerializer
from radar.models import OrganisationPatient
from radar.validation.organisation_patients import OrganisationPatientValidation
from radar.views.core import RetrieveUpdateDestroyModelView, ListCreateModelView


class OrganisationPatientListView(ListCreateModelView):
    serializer_class = OrganisationPatientSerializer
    model_class = OrganisationPatient
    validation_class = OrganisationPatientValidation


class OrganisationPatientDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = OrganisationPatientSerializer
    model_class = OrganisationPatient
    validation_class = OrganisationPatientValidation

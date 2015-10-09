from radar.api.serializers.organisation_patients import OrganisationPatientSerializer
from radar.lib.models import OrganisationPatient
from radar.lib.validation.organisation_patients import OrganisationPatientValidation
from radar.lib.views.core import RetrieveUpdateDestroyModelView, ListCreateModelView


class OrganisationPatientListView(ListCreateModelView):
    serializer_class = OrganisationPatientSerializer
    model_class = OrganisationPatient
    validation_class = OrganisationPatientValidation


class OrganisationPatientDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = OrganisationPatientSerializer
    model_class = OrganisationPatient
    validation_class = OrganisationPatientValidation

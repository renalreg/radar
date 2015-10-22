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


def register_views(app):
    app.add_url_rule('/organisation-patients', view_func=OrganisationPatientListView.as_view('organisation_patient_list'))
    app.add_url_rule('/organisation-patients/<int:id>', view_func=OrganisationPatientDetailView.as_view('organisation_patient_detail'))

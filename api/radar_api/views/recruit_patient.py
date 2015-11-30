from radar.auth.sessions import current_user
from radar.views.core import ApiView, request_json, response_json, PermissionViewMixin
from radar_api.serializers.patients import PatientSerializer
from radar.recruit_patient import recruit_patient_search, recruit_patient
from radar.validation.recruit_patient import RecruitPatientValidation, RecruitPatientSearchValidation
from radar_api.serializers.recruit_patient import RecruitPatientSearchSerializer, \
    RecruitPatientResultListSerializer, RecruitPatientSerializer
from radar.permissions import RecruitPatientPermission
from radar.recruit_patient import filter_patient_number_organisations
from radar.views.core import ListModelView
from radar_api.serializers.organisations import OrganisationSerializer
from radar.models.organisations import Organisation


class RecruitPatientSearchView(PermissionViewMixin, ApiView):
    permission_classes = [RecruitPatientPermission]

    @request_json(RecruitPatientSearchSerializer, RecruitPatientSearchValidation)
    @response_json(RecruitPatientResultListSerializer)
    def post(self, data):
        patients = recruit_patient_search(data)
        return {'patients': patients}


class RecruitPatientView(PermissionViewMixin, ApiView):
    permission_classes = [RecruitPatientPermission]

    @request_json(RecruitPatientSerializer, RecruitPatientValidation)
    @response_json(lambda: PatientSerializer(current_user))
    def post(self, data):
        patient = recruit_patient(data)
        return patient


class RecruitPatientNumberOrganisationListView(PermissionViewMixin, ApiView):
    permission_classes = [RecruitPatientPermission]

    @response_json(lambda: PatientSerializer(current_user))
    def get(self):
        organisations = get_recruit_patient_number_organisations()
        return patient


class RecruitPatientNumberOrganisationListView(ListModelView):
    serializer_class = OrganisationSerializer
    model_class = Organisation

    def filter_query(self, query):
        query = super(RecruitPatientNumberOrganisationListView, self).filter_query(query)
        query = filter_patient_number_organisations(query)
        return query


def register_views(app):
    app.add_url_rule('/recruit-patient', view_func=RecruitPatientView.as_view('recruit_patient'))
    app.add_url_rule('/recruit-patient-search', view_func=RecruitPatientSearchView.as_view('recruit_patient_search'))
    app.add_url_rule('/recruit-patient-number-organisations', view_func=RecruitPatientNumberOrganisationListView.as_view('recruit_patient_number_organisation_list'))

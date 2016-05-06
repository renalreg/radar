from radar.auth.sessions import current_user
from radar.api.views.core import ApiView, request_json, response_json, PermissionViewMixin
from radar_api.serializers.patients import PatientSerializer
from radar.validation.recruit_patient import RecruitPatientValidation, RecruitPatientSearchValidation
from radar_api.serializers.recruit_patient import RecruitPatientSearchSerializer, RecruitPatientResultSerializer, RecruitPatientSerializer
from radar.api.permissions import RecruitPatientPermission
from radar_recruitment import SearchPatient, RecruitmentPatient, DemographicsMismatch
from radar.validation.core import ValidationError


def mismatch_error(e):
    message = (
        "Found an existing patient (RaDaR {}) with this patient number. "
        "The name, date of birth or gender you have supplied don't match the details we hold. "
        "Please contact RaDaR support for help recruiting this patient."
    ).format(e.patient.id)

    return ValidationError({'number': message})


class RecruitPatientSearchView(PermissionViewMixin, ApiView):
    permission_classes = [RecruitPatientPermission]

    @request_json(RecruitPatientSearchSerializer, RecruitPatientSearchValidation)
    @response_json(lambda: RecruitPatientResultSerializer(current_user))
    def post(self, data):
        search_patient = SearchPatient(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            date_of_birth=data.get('date_of_birth'),
            gender=data.get('gender'),
            number_group=data.get('number_group'),
            number=data.get('number'),
        )

        try:
            patient = search_patient.search_radar()
        except DemographicsMismatch as e:
            raise mismatch_error(e)

        return {'patient': patient}


class RecruitPatientView(PermissionViewMixin, ApiView):
    permission_classes = [RecruitPatientPermission]

    @request_json(RecruitPatientSerializer, RecruitPatientValidation)
    @response_json(lambda: PatientSerializer(current_user))
    def post(self, data):
        search_patient = SearchPatient(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            date_of_birth=data.get('date_of_birth'),
            gender=data.get('gender'),
            number_group=data.get('number_group'),
            number=data.get('number'),
        )

        recruitment_patient = RecruitmentPatient(
            search_patient=search_patient,
            hospital_group=data.get('hospital_group'),
            cohort_group=data.get('cohort_group'),
            ethnicity=data.get('ethnicity')
        )

        try:
            patient = recruitment_patient.save()
        except DemographicsMismatch as e:
            raise mismatch_error(e)

        return patient


def register_views(app):
    app.add_url_rule('/recruit-patient-search', view_func=RecruitPatientSearchView.as_view('recruit_patient_search'))
    app.add_url_rule('/recruit-patient', view_func=RecruitPatientView.as_view('recruit_patient'))

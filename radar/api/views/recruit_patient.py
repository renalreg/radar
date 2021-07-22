from cornflake.exceptions import ValidationError

from radar.api.permissions import RecruitPatientPermission
from radar.api.serializers.patients import PatientSerializer
from radar.api.serializers.recruit_patient import (
    RecruitPatientResultSerializer,
    RecruitPatientSearchSerializer,
    RecruitPatientSerializer
)
from radar.api.views.generics import ApiView, PermissionViewMixin, request_json, response_json
from radar.recruitment import DemographicsMismatch, RecruitmentPatient, SearchPatient


def mismatch_error(e):
    message = (
        "Found an existing patient (ID {}) with this patient number. "
        "The name, date of birth or gender you have supplied don't match the details we hold. "
        "Please contact RaDaR support for help recruiting this patient."
    ).format(e.patient.id)

    return ValidationError({'number': message})


class RecruitPatientSearchView(PermissionViewMixin, ApiView):
    """Search for an existing patient."""

    permission_classes = [RecruitPatientPermission]

    @request_json(RecruitPatientSearchSerializer)
    @response_json(RecruitPatientResultSerializer)
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
    """Add a patient to a cohort and hospital."""

    permission_classes = [RecruitPatientPermission]

    @request_json(RecruitPatientSerializer)
    @response_json(PatientSerializer)
    def post(self, data):
        search_patient = SearchPatient(
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=data['date_of_birth'],
            gender=data['gender'],
            number_group=data['number_group'],
            number=data['number'],
        )

        recruitment_patient = RecruitmentPatient(
            search_patient=search_patient,
            hospital_group=data['hospital_group'],
            cohort_group=data['cohort_group'],
            consents=data['consents'],
            diagnosis=data['diagnosis'],
            nationality=data['nationality'],
            ethnicity=data['ethnicity'],
        )

        try:
            patient = recruitment_patient.save()
        except DemographicsMismatch as e:
            raise mismatch_error(e)

        return patient


def register_views(app):
    app.add_url_rule('/recruit-patient-search', view_func=RecruitPatientSearchView.as_view('recruit_patient_search'))
    app.add_url_rule('/recruit-patient', view_func=RecruitPatientView.as_view('recruit_patient'))

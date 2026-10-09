from cornflake.exceptions import ValidationError

from radar.api.permissions import RecruitPatientPermission
from radar.api.serializers.patients import PatientSerializer
from radar.api.serializers.recruit_patient import (
    RecruitPatientResultSerializer,
    RecruitPatientSearchSerializer,
    RecruitPatientSerializer,
)
from radar.api.views.generics import (
    ApiView,
    PermissionViewMixin,
    request_json,
    response_json,
)
from radar.recruitment import DemographicsMismatch, RecruitmentPatient, SearchPatient
from radar.variants import IS_INTERNATIONAL


def mismatch_error(e):
    message = (
        f"Found an existing patient (ID {e.patient.id}) with this patient number. "
        "The name, date of birth or gender you have supplied don't match the details we hold. "
        "Please contact RaDaR support for help recruiting this patient."
    )

    return ValidationError({"number": message})


class RecruitPatientSearchView(PermissionViewMixin, ApiView):
    """Search for an existing patient."""

    permission_classes = [RecruitPatientPermission]

    @request_json(RecruitPatientSearchSerializer)
    @response_json(RecruitPatientResultSerializer)
    def post(self, data):
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "number_group",
            "number",
        ]
        if not IS_INTERNATIONAL:
            fields.append("email_address")

        search_patient = SearchPatient(**{name: data.get(name) for name in fields})

        try:
            patient = search_patient.search_radar()
        except DemographicsMismatch as e:
            raise mismatch_error(e)

        return {"patient": patient}


class RecruitPatientView(PermissionViewMixin, ApiView):
    """Add a patient to a cohort and hospital."""

    permission_classes = [RecruitPatientPermission]

    @request_json(RecruitPatientSerializer)
    @response_json(PatientSerializer)
    def post(self, data):
        search_fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "number_group",
            "number",
        ]
        recruitment_fields = [
            "hospital_group",
            "cohort_group",
            "consents",
            "diagnosis",
            "nationality",
            "ethnicity",
        ]

        if not IS_INTERNATIONAL:
            search_fields.append("email_address")
            recruitment_fields.append("email_reason")

        search_patient = SearchPatient(**{name: data[name] for name in search_fields})

        recruitment_patient = RecruitmentPatient(
            search_patient=search_patient,
            **{name: data[name] for name in recruitment_fields},
        )

        try:
            patient = recruitment_patient.save()
        except DemographicsMismatch as e:
            raise mismatch_error(e)

        return patient


def register_views(app):
    app.add_url_rule(
        "/recruit-patient-search",
        view_func=RecruitPatientSearchView.as_view("recruit_patient_search"),
    )
    app.add_url_rule(
        "/recruit-patient", view_func=RecruitPatientView.as_view("recruit_patient")
    )

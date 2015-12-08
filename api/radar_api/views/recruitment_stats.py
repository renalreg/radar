from flask import request

from radar.cohorts import get_radar_cohort
from radar_api.serializers.recruitment_stats import DataPointListSerializer, CohortRecruitmentRequestSerializer, \
    OrganisationRecruitmentRequestSerializer, RecruitByCohortListSerializer, RecruitmentByCohortRequestSerializer, \
    RecruitByOrganisationListSerializer, RecruitmentByOrganisationRequestSerializer
from radar.models import CohortPatient, OrganisationPatient
from radar.recruitment_stats import recruitment_by_month, recruitment_by_cohort, recruitment_by_organisation
from radar.validation.core import ValidationError
from radar.views.core import response_json, ApiView


class CohortRecruitmentTimelineView(ApiView):
    @response_json(DataPointListSerializer)
    def get(self):
        serializer = CohortRecruitmentRequestSerializer()
        args = serializer.args_to_value(request.args)

        cohort = args.get('cohort')

        if cohort is None:
            raise ValidationError({'cohort': 'This field is required.'})

        points = recruitment_by_month(CohortPatient.created_date, [CohortPatient.cohort == cohort])

        return {'points': points}


class OrganisationRecruitmentTimelineView(ApiView):
    @response_json(DataPointListSerializer)
    def get(self):
        serializer = OrganisationRecruitmentRequestSerializer()
        args = serializer.args_to_value(request.args)

        organisation = args.get('organisation')

        if organisation is None:
            raise ValidationError({'organisation': 'This field is required.'})

        points = recruitment_by_month(OrganisationPatient.created_date, [OrganisationPatient.organisation == organisation])

        return {'points': points}


class PatientRecruitmentTimelineView(ApiView):
    @response_json(DataPointListSerializer)
    def get(self):
        cohort = get_radar_cohort()
        points = recruitment_by_month(CohortPatient.recruited_date, [CohortPatient.cohort == cohort])
        return {'points': points}


class RecruitmentByCohortView(ApiView):
    @response_json(RecruitByCohortListSerializer)
    def get(self):
        serializer = RecruitmentByCohortRequestSerializer()
        args = serializer.args_to_value(request.args)

        organisation = args.get('organisation')

        filters = []

        if organisation is not None:
            filters.append(OrganisationPatient.organisation == organisation)

        counts = recruitment_by_cohort(filters)
        counts = [{'cohort': cohort, 'patientCount': count} for cohort, count in counts]

        return {'counts': counts}


class RecruitmentByOrganisationView(ApiView):
    @response_json(RecruitByOrganisationListSerializer)
    def get(self):
        serializer = RecruitmentByOrganisationRequestSerializer()
        args = serializer.args_to_value(request.args)

        cohort = args.get('cohort')

        filters = []

        if cohort is not None:
            filters.append(CohortPatient.cohort == cohort)

        counts = recruitment_by_organisation(filters)
        counts = [{'organisation': organisation, 'patientCount': count} for organisation, count in counts]

        return {'counts': counts}


def register_views(app):
    app.add_url_rule('/cohort-recruitment-timeline', view_func=CohortRecruitmentTimelineView.as_view('cohort_recruitment_timeline'))
    app.add_url_rule('/organisation-recruitment-timeline', view_func=OrganisationRecruitmentTimelineView.as_view('organisation_recruitment_timeline'))
    app.add_url_rule('/patient-recruitment-timeline', view_func=PatientRecruitmentTimelineView.as_view('patient_recruitment_timeline'))
    app.add_url_rule('/recruitment-by-cohort', view_func=RecruitmentByCohortView.as_view('recruitment_by_cohort'))
    app.add_url_rule('/recruitment-by-organisation', view_func=RecruitmentByOrganisationView.as_view('recruitment_by_organisation'))

from flask import request

from radar.api.serializers.recruitment_stats import DataPointsSerializer, CohortRecruitmentRequestSerializer, \
    OrganisationRecruitmentRequestSerializer
from radar.lib.models import CohortPatient, OrganisationPatient, Patient
from radar.lib.recruitment_stats import recruitment_by_month
from radar.lib.validation.core import ValidationError
from radar.lib.views.core import response_json, ApiView


class CohortRecruitmentStatsView(ApiView):
    @response_json(DataPointsSerializer)
    def get(self):
        serializer = CohortRecruitmentRequestSerializer()
        args = serializer.args_to_value(request.args)

        cohort = args.get('cohort')

        if cohort is None:
            raise ValidationError({'cohort': 'This field is required.'})

        points = recruitment_by_month(CohortPatient.created_date, [CohortPatient.cohort == cohort])

        return {'points': points}


class OrganisationRecruitmentStatsView(ApiView):
    @response_json(DataPointsSerializer)
    def get(self):
        serializer = OrganisationRecruitmentRequestSerializer()
        args = serializer.args_to_value(request.args)

        organisation = args.get('organisation')

        if organisation is None:
            raise ValidationError({'organisation': 'This field is required.'})

        points = recruitment_by_month(OrganisationPatient.created_date, [OrganisationPatient.organisation == organisation])

        return {'points': points}


class PatientRecruitmentStatsView(ApiView):
    @response_json(DataPointsSerializer)
    def get(self):
        points = recruitment_by_month(Patient.created_date)
        return {'points': points}

from flask import request

from radar.groups import get_radar_group
from radar_api.serializers.recruitment_stats import DataPointListSerializer,\
    GroupRecruitmentRequestSerializer, RecruitmentByGroupListSerializer,\
    RecruitmentByGroupRequestSerializer
from radar.models.groups import GroupPatient
from radar.recruitment_stats import recruitment_by_month, recruitment_by_group
from radar.validation.core import ValidationError
from radar.views.core import response_json, ApiView


class GroupRecruitmentTimelineView(ApiView):
    @response_json(DataPointListSerializer)
    def get(self):
        serializer = GroupRecruitmentRequestSerializer()
        args = serializer.args_to_value(request.args)

        group = args.get('group')

        if group is None:
            raise ValidationError({'group': 'This field is required.'})

        points = recruitment_by_month(GroupPatient.from_date, [GroupPatient.group == group])

        return {'points': points}


class PatientRecruitmentTimelineView(ApiView):
    @response_json(DataPointListSerializer)
    def get(self):
        group = get_radar_group()
        points = recruitment_by_month(GroupPatient.from_date, [GroupPatient.group == group])
        return {'points': points}


class RecruitmentByGroupView(ApiView):
    @response_json(RecruitmentByGroupListSerializer)
    def get(self):
        serializer = RecruitmentByGroupRequestSerializer()
        args = serializer.args_to_value(request.args)

        filter_by_group = args.get('group')

        filters = []

        if filter_by_group is not None:
            filters.append(GroupPatient.group == filter_by_group)

        counts = recruitment_by_group(filters)
        counts = [{'group': group, 'patientCount': count} for group, count in counts]

        return {'counts': counts}


def register_views(app):
    app.add_url_rule('/group-recruitment-timeline', view_func=GroupRecruitmentTimelineView.as_view('group_recruitment_timeline'))
    app.add_url_rule('/patient-recruitment-timeline', view_func=PatientRecruitmentTimelineView.as_view('patient_recruitment_timeline'))
    app.add_url_rule('/recruitment-by-group', view_func=RecruitmentByGroupView.as_view('recruitment_by_group'))

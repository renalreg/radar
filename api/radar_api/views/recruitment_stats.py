from flask import request

from radar.groups import get_radar_group
from radar_api.serializers.recruitment_stats import DataPointListSerializer,\
    RecruitmentTimelineRequestSerializer, RecruitmentByGroupListSerializer,\
    RecruitmentByGroupRequestSerializer
from radar.models.groups import GroupPatient
from radar.recruitment_stats import recruitment_by_month, recruitment_by_group
from radar.views.core import response_json, ApiView


class RecruitmentTimelineView(ApiView):
    @response_json(DataPointListSerializer)
    def get(self):
        serializer = RecruitmentTimelineRequestSerializer()
        args = serializer.args_to_value(request.args)

        group = args.get('group')

        if group is None:
            group = get_radar_group()

        points = recruitment_by_month(GroupPatient.from_date, [GroupPatient.group == group])

        return {'points': points}


class RecruitmentByGroupView(ApiView):
    @response_json(RecruitmentByGroupListSerializer)
    def get(self):
        serializer = RecruitmentByGroupRequestSerializer()
        args = serializer.args_to_value(request.args)

        counts = recruitment_by_group(args.get('group'), args.get('group_type'))
        counts = [{'group': group, 'patientCount': count} for group, count in counts]

        return {'counts': counts}


def register_views(app):
    app.add_url_rule('/recruitment-timeline', view_func=RecruitmentTimelineView.as_view('recruitment_timeline'))
    app.add_url_rule('/recruitment-by-group', view_func=RecruitmentByGroupView.as_view('recruitment_by_group'))

from flask import request

from radar.groups import get_radar_group
from radar_api.serializers.stats import DataPointListSerializer,\
    RecruitmentByMonthRequestSerializer, PatientsByGroupListSerializer,\
    PatientsByGroupRequestSerializer, PatientsByRecruitedGroupRequestSerializer
from radar.stats import patients_by_group, recruitment_by_month, patients_by_recruited_group
from radar.views.core import response_json, ApiView


class RecruitmentByMonthView(ApiView):
    @response_json(DataPointListSerializer)
    def get(self):
        serializer = RecruitmentByMonthRequestSerializer()
        args = serializer.args_to_value(request.args)

        group = args.get('group')

        if group is None:
            group = get_radar_group()

        points = recruitment_by_month(group)

        return {'points': points}


class PatientsByGroupView(ApiView):
    @response_json(PatientsByGroupListSerializer)
    def get(self):
        serializer = PatientsByGroupRequestSerializer()
        args = serializer.args_to_value(request.args)

        counts = patients_by_group(args.get('group'), args.get('group_type'))
        counts = [{'group': group, 'count': count} for group, count in counts]

        return {'counts': counts}


class PatientsByRecruitedGroupView(ApiView):
    @response_json(PatientsByGroupListSerializer)
    def get(self):
        serializer = PatientsByRecruitedGroupRequestSerializer()
        args = serializer.args_to_value(request.args)

        group = args.get('group')

        if group is None:
            group = get_radar_group()

        counts = patients_by_recruited_group(group)
        counts = [{'group': x, 'count': y} for x, y in counts]

        return {'counts': counts}


def register_views(app):
    app.add_url_rule('/recruitment-by-month', view_func=RecruitmentByMonthView.as_view('recruitment_by_month'))
    app.add_url_rule('/patients-by-group', view_func=PatientsByGroupView.as_view('patients_by_group'))
    app.add_url_rule('/patients-by-recruited-group', view_func=PatientsByRecruitedGroupView.as_view('patients_by_recruited_group'))

from cornflake import fields, serializers

from radar.api.serializers.common import GroupField
from radar.api.serializers.stats import DataPointListSerializer, PatientsByGroupListSerializer
from radar.api.views.generics import response_json, ApiView, parse_args
from radar.models.groups import Group, GROUP_TYPE
from radar.stats import patients_by_group, recruitment_by_month, patients_by_recruited_group


class RecruitmentByMonthRequestSerializer(serializers.Serializer):
    group = GroupField(required=False)


class PatientsByGroupRequestSerializer(serializers.Serializer):
    group = GroupField(required=False)
    group_type = fields.EnumField(GROUP_TYPE, required=False)


class PatientsByRecruitedGroupRequestSerializer(serializers.Serializer):
    group = GroupField(required=False)


class RecruitmentByMonthView(ApiView):
    @response_json(DataPointListSerializer)
    def get(self):
        args = parse_args(RecruitmentByMonthRequestSerializer)

        if args['group'] is not None:
            group = args['group']
        else:
            group = Group.get_radar()

        points = recruitment_by_month(group)

        return {'points': points}


class PatientsByGroupView(ApiView):
    @response_json(PatientsByGroupListSerializer)
    def get(self):
        args = parse_args(PatientsByGroupRequestSerializer)

        counts = patients_by_group(args['group'], args['group_type'])
        counts = [{'group': group, 'count': count} for group, count in counts]

        return {'counts': counts}


class PatientsByRecruitedGroupView(ApiView):
    @response_json(PatientsByGroupListSerializer)
    def get(self):
        args = parse_args(PatientsByRecruitedGroupRequestSerializer)

        if args['group'] is not None:
            group = args['group']
        else:
            group = Group.get_radar()

        counts = patients_by_recruited_group(group)
        counts = [{'group': x, 'count': y} for x, y in counts]

        return {'counts': counts}


def register_views(app):
    app.add_url_rule('/recruitment-by-month', view_func=RecruitmentByMonthView.as_view('recruitment_by_month'))
    app.add_url_rule('/patients-by-group', view_func=PatientsByGroupView.as_view('patients_by_group'))
    app.add_url_rule('/patients-by-recruited-group', view_func=PatientsByRecruitedGroupView.as_view('patients_by_recruited_group'))

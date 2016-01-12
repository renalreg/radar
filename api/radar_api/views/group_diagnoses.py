from flask import request
from radar_api.serializers.diagnoses import GroupDiagnosisSerializer, GroupDiagnosisRequestSerializer
from radar.models.diagnoses import GroupDiagnosis
from radar.views.core import ListModelView


class GroupDiagnosisListView(ListModelView):
    serializer_class = GroupDiagnosisSerializer
    model_class = GroupDiagnosis

    def filter_query(self, query):
        query = super(GroupDiagnosisListView, self).filter_query(query)

        serializer = GroupDiagnosisRequestSerializer()
        args = serializer.args_to_value(request.args)

        group_id = args.get('group')

        if group_id is not None:
            query = query.filter(GroupDiagnosis.group_id == group_id)

        return query


def register_views(app):
    app.add_url_rule('/group-diagnoses', view_func=GroupDiagnosisListView.as_view('group_diagnosis_list'))

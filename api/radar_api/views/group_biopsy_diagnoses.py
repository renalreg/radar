from flask import request
from radar_api.serializers.diagnoses import GroupBiopsyDiagnosisSerializer, GroupBiopsyDiagnosisRequestSerializer
from radar.models.diagnoses import BiopsyDiagnosis, GroupBiopsyDiagnosis
from radar.views.core import ListModelView


class GroupBiopsyDiagnosisListView(ListModelView):
    serializer_class = GroupBiopsyDiagnosisSerializer
    model_class = GroupBiopsyDiagnosis

    def filter_query(self, query):
        query = super(GroupBiopsyDiagnosisListView, self).filter_query(query)

        serializer = GroupBiopsyDiagnosisRequestSerializer()
        args = serializer.args_to_value(request.args)

        group_id = args.get('group')

        if group_id is not None:
            query = query.join(BiopsyDiagnosis.group_biopsy_diagnoses)
            query = query.filter(GroupBiopsyDiagnosis.group_id == group_id)

        return query


def register_views(app):
    app.add_url_rule('/group-biopsy-diagnoses', view_func=GroupBiopsyDiagnosisListView.as_view('group_biopsy_diagnosis_list'))

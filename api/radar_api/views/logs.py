from sqlalchemy import Integer, or_, and_
from flask import request

from radar_api.serializers.logs import LogSerializer, LogListRequestSerializer
from radar.models.logs import Log
from radar.permissions import AdminPermission
from radar.views.core import ListModelView, RetrieveModelView


class LogListView(ListModelView):
    serializer_class = LogSerializer
    model_class = Log
    permission_classes = [AdminPermission]
    sort_fields = ['date']

    def filter_query(self, query):
        query = super(LogListView, self).filter_query(query)

        serializer = LogListRequestSerializer()
        args = serializer.args_to_value(request.args)

        from_date = args.get('from_date')
        to_date = args.get('to_date')
        type = args.get('type')
        user_id = args.get('user')
        patient_id = args.get('patient')
        table_name = args.get('table_name')

        if from_date is not None:
            query = query.filter(Log.date >= from_date)

        if to_date is not None:
            query = query.filter(Log.date <= to_date)

        if type is not None:
            query = query.filter(Log.type == type)

        if user_id is not None:
            query = query.filter(Log.user_id == user_id)

        if patient_id is not None:
            query = query.filter(or_(
                and_(Log.type == 'VIEW_PATIENT', Log.data['patient_id'].astext.cast(Integer) == patient_id),
                and_(Log.type == 'INSERT', Log.data[('new_data', 'patient_id')].astext.cast(Integer) == patient_id),
                and_(Log.type == 'UPDATE', Log.data[('original_data', 'patient_id')].astext.cast(Integer) == patient_id),
                and_(Log.type == 'UPDATE', Log.data[('new_data', 'patient_id')].astext.cast(Integer) == patient_id),
                and_(Log.type == 'DELETE', Log.data[('original_data', 'patient_id')].astext.cast(Integer) == patient_id),
            ))

        if table_name is not None:
            query = query.filter(
                Log.type.in_(['INSERT', 'UPDATE', 'DELETE']),
                Log.data['table_name'].astext == table_name
            )

        return query


class LogDetailView(RetrieveModelView):
    serializer_class = LogSerializer
    model_class = Log
    permission_classes = [AdminPermission]


def register_views(app):
    app.add_url_rule('/logs', view_func=LogListView.as_view('log_list'))
    app.add_url_rule('/logs/<int:id>', view_func=LogDetailView.as_view('log_detail'))

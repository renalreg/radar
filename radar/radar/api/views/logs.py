from sqlalchemy import Integer, or_, and_
from cornflake.exceptions import ValidationError
from cornflake import fields, serializers

from radar.models.logs import Log
from radar.models.users import User
from radar.api.serializers.logs import LogSerializer
from radar.api.permissions import AdminPermission
from radar.api.views.generics import ListModelView, RetrieveModelView, parse_args


class LogListRequestSerializer(serializers.Serializer):
    from_date = fields.DateTimeField(required=False)
    to_date = fields.DateTimeField(required=False)
    type = fields.StringField(required=False)
    user = fields.IntegerField(required=False)
    patient = fields.IntegerField(required=False)
    table_name = fields.StringField(required=False)
    username = fields.StringField(required=False)


class LogListView(ListModelView):
    serializer_class = LogSerializer
    model_class = Log
    permission_classes = [AdminPermission]
    sort_fields = ['date']

    def filter_query(self, query):
        query = super(LogListView, self).filter_query(query)

        args = parse_args(LogListRequestSerializer)

        if args['from_date'] is not None:
            query = query.filter(Log.date >= args['from_date'])

        if args['to_date'] is not None:
            query = query.filter(Log.date <= args['to_date'])

        if args['type'] is not None:
            query = query.filter(Log.type == args['type'])

        if args['user'] is not None:
            query = query.filter(Log.user_id == args['user'])

        if args['username'] is not None:
            user = User.query.filter(User.username == args['username']).first()

            if user is None:
                raise ValidationError({'username': 'User not found!'})

            query = query.filter(Log.user == user)

        if args['patient'] is not None:
            patient_id = args['patient']

            query = query.filter(or_(
                and_(Log.type == 'VIEW_PATIENT', Log.data['patient_id'].astext.cast(Integer) == patient_id),
                and_(Log.type == 'INSERT', Log.data[('new_data', 'patient_id')].astext.cast(Integer) == patient_id),
                and_(Log.type == 'UPDATE', Log.data[('original_data', 'patient_id')].astext.cast(Integer) == patient_id),
                and_(Log.type == 'UPDATE', Log.data[('new_data', 'patient_id')].astext.cast(Integer) == patient_id),
                and_(Log.type == 'DELETE', Log.data[('original_data', 'patient_id')].astext.cast(Integer) == patient_id),
            ))

        if args['table_name']:
            query = query.filter(
                Log.type.in_(['INSERT', 'UPDATE', 'DELETE']),
                Log.data['table_name'].astext == args['table_name']
            )

        return query


class LogDetailView(RetrieveModelView):
    serializer_class = LogSerializer
    model_class = Log
    permission_classes = [AdminPermission]


def register_views(app):
    app.add_url_rule('/logs', view_func=LogListView.as_view('log_list'))
    app.add_url_rule('/logs/<int:id>', view_func=LogDetailView.as_view('log_detail'))

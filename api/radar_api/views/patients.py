from flask import request

from radar_api.serializers.patients import PatientSerializer, PatientListRequestSerializer
from radar.patient_search import PatientQueryBuilder
from radar.permissions import PatientPermission
from radar.views.core import ListModelView, RetrieveUpdateModelView
from radar.models import Patient
from radar.auth.sessions import current_user


class PatientListView(ListModelView):
    model_class = Patient
    permission_classes = [PatientPermission]

    def get_query(self):
        serializer = PatientListRequestSerializer()
        args = serializer.args_to_value(request.args)

        builder = PatientQueryBuilder(current_user)

        if args.get('id') is not None:
            builder.patient_id(args['id'])

        if args.get('first_name'):
            builder.first_name(args['first_name'])

        if args.get('last_name'):
            builder.last_name(args['last_name'])

        if args.get('organisation') is not None:
            if args.get('is_active') is not None:
                builder.organisation(args['organisation'], args['is_active'])
            else:
                builder.organisation(args['organisation'])

        if args.get('cohort') is not None:
            if args.get('is_active') is not None:
                builder.cohort(args['cohort'], args['is_active'])
            else:
                builder.cohort(args['cohort'])

        if args.get('patient_number'):
            builder.patient_number(args['patient_number'])

        if args.get('gender'):
            builder.gender(args['gender'])

        if args.get('date_of_birth') is not None:
            builder.date_of_birth(args['date_of_birth'])

        if args.get('year_of_birth') is not None:
            builder.year_of_birth(args['year_of_birth'])

        if args.get('date_of_death') is not None:
            builder.date_of_death(args['date_of_death'])

        if args.get('year_of_death') is not None:
            builder.year_of_death(args['year_of_death'])

        if args.get('is_active') is not None:
            builder.is_active(args['is_active'])

        sort, reverse = self.get_sort_args()

        if sort is not None:
            builder.sort(sort, reverse)

        query = builder.build()

        return query

    def get_serializer(self):
        return PatientSerializer(current_user)


class PatientDetailView(RetrieveUpdateModelView):
    model_class = Patient
    permission_classes = [PatientPermission]

    def get_query(self):
        builder = PatientQueryBuilder(current_user)
        return builder.build()

    def get_serializer(self):
        return PatientSerializer(current_user)


def register_views(app):
    app.add_url_rule('/patients', view_func=PatientListView.as_view('patient_list'))
    app.add_url_rule('/patients/<int:id>', view_func=PatientDetailView.as_view('patient_detail'))

from flask import request

from radar_api.serializers.patients import PatientSerializer, PatientListRequestSerializer, TinyPatientSerializer
from radar.patient_search import PatientQueryBuilder
from radar.permissions import PatientPermission
from radar.views.core import ListModelView, RetrieveUpdateModelView
from radar.models.patients import Patient
from radar.auth.sessions import current_user


class PatientListView(ListModelView):
    model_class = Patient
    permission_classes = [PatientPermission]

    def get_query(self):
        serializer = PatientListRequestSerializer()
        args = serializer.args_to_value(request.args)

        builder = PatientQueryBuilder(current_user)

        patient_id = args.get('id')
        first_name = args.get('first_name') or None
        last_name = args.get('last_name') or None
        patient_number = args.get('patient_number') or None
        gender = args.get('gender') or None
        date_of_birth = args.get('date_of_birth')
        year_of_birth = args.get('year_of_birth')
        date_of_death = args.get('date_of_death')
        year_of_death = args.get('year_of_death')
        groups = args.get('group') or []
        current = args.get('current')

        if patient_id is not None:
            builder.patient_id(patient_id)

        if first_name is not None:
            builder.first_name(first_name)

        if last_name is not None:
            builder.last_name(last_name)

        if patient_number is not None:
            builder.patient_number(patient_number)

        if gender is not None:
            builder.gender(gender)

        if date_of_birth is not None:
            builder.date_of_birth(date_of_birth)

        if year_of_birth is not None:
            builder.year_of_birth(year_of_birth)

        if date_of_death is not None:
            builder.date_of_death(date_of_death)

        if year_of_death is not None:
            builder.year_of_death(year_of_death)

        for group in groups:
            builder.group(group, current=current)

        sort, reverse = self.get_sort_args()

        if sort is not None:
            builder.sort(sort, reverse)

        query = builder.build(current=current)

        return query

    def get_serializer(self):
        return TinyPatientSerializer(current_user)


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

from flask import request

from radar.api.serializers.patients import PatientSerializer, PatientListRequestSerializer
from radar.lib.patient_search import PatientQueryBuilder
from radar.lib.patients import PatientProxy
from radar.lib.permissions import PatientPermission
from radar.lib.views.core import RetrieveUpdateDestroyModelView, ListModelView
from radar.lib.models import Patient
from radar.lib.auth.sessions import current_user


class PatientListView(ListModelView):
    serializer_class = PatientSerializer
    model_class = Patient
    permission_classes = [PatientPermission]

    def get_query(self):
        serializer = PatientListRequestSerializer()
        args = serializer.args_to_value(request.args)

        builder = PatientQueryBuilder(current_user)

        if 'id' in args:
            builder.patient_id(args['id'])

        if 'first_name' in args:
            builder.first_name(args['first_name'])

        if 'last_name' in args:
            builder.last_name(args['last_name'])

        if 'organisation' in args:
            if 'is_active' in args:
                builder.organisation(args['organisation'], args['is_active'])
            else:
                builder.organisation(args['organisation'])

        if 'cohort' in args:
            if 'is_active' in args:
                builder.cohort(args['cohort'], args['is_active'])
            else:
                builder.cohort(args['cohort'])

        if 'patient_number' in args:
            builder.patient_number(args['patient_number'])

        if 'gender' in args:
            builder.gender(args['gender'])

        if 'date_of_birth' in args:
            builder.date_of_birth(args['date_of_birth'])

        if 'year_of_birth' in args:
            builder.year_of_birth(args['year_of_birth'])

        if 'date_of_death' in args:
            builder.date_of_death(args['date_of_death'])

        if 'year_of_death' in args:
            builder.year_of_death(args['year_of_death'])

        if 'is_active' in args:
            builder.is_active(args['is_active'])

        sort, reverse = self.get_sort_args()

        if sort is not None:
            builder.sort(sort, reverse)

        query = builder.build()

        return query

    def get_object_list(self):
        patients, pagination = super(PatientListView, self).get_object_list()

        # Wrap patients in proxy object
        patients = [PatientProxy(x, current_user) for x in patients]

        return patients, pagination


class PatientDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = PatientSerializer
    model_class = Patient
    permission_classes = [PatientPermission]

    def get_query(self):
        builder = PatientQueryBuilder(current_user)
        return builder.build()

    def get_object(self):
        patient = super(PatientDetailView, self).get_object()
        return PatientProxy(patient, current_user)

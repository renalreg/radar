from flask import request

from sqlalchemy.orm import aliased

from radar_api.serializers.consultants import ConsultantSerializer, ConsultantRequestSerializer
from radar.views.core import ListModelView, RetrieveModelView, UpdateModelView, DestroyModelView, CreateModelView
from radar.models.consultants import Consultant, GroupConsultant
from radar.permissions import AdminPermission
from radar.validation.consultants import ConsultantValidation
from radar.database import db
from radar.models.groups import Group, GroupPatient
from radar.patient_search import PatientQueryBuilder
from radar.auth.sessions import current_user
from radar.models.patients import Patient


def filter_consultants_by_patient_id(query, patient_id):
    # Only return consultants that belong to one of the groups the patient also belongs to
    consultant_alias = aliased(Consultant)
    consultants_for_patient_query = db.session.query(consultant_alias)\
        .join(consultant_alias.group_consultants)\
        .join(GroupConsultant.group)\
        .join(Group.group_patients)\
        .filter(
            GroupPatient.patient_id == patient_id,
            Consultant.id == consultant_alias.id
        )
    query = query.filter(consultants_for_patient_query.exists())

    # Check the user has permission to view this patient
    patient_query = PatientQueryBuilder(current_user).build()
    patient_query = patient_query.filter(Patient.id == patient_id)
    query = query.filter(patient_query.exists())

    return query


class ConsultantListView(ListModelView):
    serializer_class = ConsultantSerializer
    model_class = Consultant

    def filter_query(self, query):
        query = super(ConsultantListView, self).filter_query(query)

        serializer = ConsultantRequestSerializer()
        args = serializer.args_to_value(request.args)

        # Consultants available to a patient
        if 'patient' in args:
            patient_id = args['patient']
            query = filter_consultants_by_patient_id(query, patient_id)

        return query


class ConsultantCreateView(CreateModelView):
    serializer_class = ConsultantSerializer
    model_class = Consultant
    validation_class = ConsultantValidation


class ConsultantRetrieveView(RetrieveModelView):
    serializer_class = ConsultantSerializer
    model_class = Consultant


class ConsultantUpdateView(UpdateModelView):
    serializer_class = ConsultantSerializer
    model_class = Consultant
    validation_class = ConsultantValidation
    permissions = [AdminPermission]


class ConsultantDestroyView(DestroyModelView):
    serializer_class = ConsultantSerializer
    model_class = Consultant
    permissions = [AdminPermission]


def register_views(app):
    app.add_url_rule('/consultants', view_func=ConsultantListView.as_view('consultant_list'))
    app.add_url_rule('/consultants', view_func=ConsultantCreateView.as_view('consultant_create'))
    app.add_url_rule('/consultants/<id>', view_func=ConsultantRetrieveView.as_view('consultant_retrieve'))
    app.add_url_rule('/consultants/<id>', view_func=ConsultantUpdateView.as_view('consultant_update'))
    app.add_url_rule('/consultants/<id>', view_func=ConsultantDestroyView.as_view('consultant_destroy'))

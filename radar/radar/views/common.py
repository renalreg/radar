from flask import request
from cornflake import fields, serializers
from sqlalchemy import or_, and_
from sqlalchemy.orm import aliased

from radar.views.generics import (
    ListView,
    ListCreateModelView,
    RetrieveUpdateDestroyModelView
)
from radar.database import db
from radar.auth.sessions import current_user
from radar.models.groups import Group, GroupPatient, GroupUser, GROUP_TYPE
from radar.models.patients import Patient
from radar.models.users import User
from radar.permissions import (
    GroupObjectPermission,
    PatientObjectPermission,
    RadarSourceObjectPermission,
    SourceObjectPermission
)
from radar.user_search import UserQueryBuilder
from radar.patient_search import PatientQueryBuilder, filter_by_permissions
from radar.roles import get_roles_with_permission, PERMISSION
from radar.views.generics import parse_args


class StringLookupListView(ListView):
    items = {}

    def get_items(self):
        return self.items

    def get_serializer(self):
        return fields.StringLookupField()

    def get_object_list(self):
        return self.get_items().keys()


class IntegerLookupListView(ListView):
    items = {}

    def get_items(self):
        return self.items

    def get_serializer(self):
        return fields.IntegerLookupField()

    def get_object_list(self):
        return self.get_items().keys()


def filter_query_by_group_permissions(query, model_class):
    # Filter the query based on the user's group membership
    # Admins can view all data so don't filter their queries
    if not current_user.is_admin:
        group_a = aliased(Group)
        group_b = aliased(Group)

        # Check if the user has permission through their group membership (requires the VIEW_PATIENT permission)
        # If the user has the VIEW_PATIENT permission on one of the patient's hospitals they can view all cohort data
        sub_query = db.session.query(Group)\
            .join(group_b, GroupPatient.group)\
            .join(Group.group_users)\
            .filter(
                GroupPatient.patient_id == model_class.patient_id,
                GroupUser.user == current_user,
                GroupUser.role.in_(get_roles_with_permission(PERMISSION.VIEW_PATIENT)),
                or_(
                    GroupPatient.group_id == model_class.group_id,
                    and_(
                        group_a.type == GROUP_TYPE.COHORT,
                        group_b.type == GROUP_TYPE.HOSPITAL
                    )
                )
            )\
            .exists()

        # Filter the query to only include rows the user has permission to see
        query = query.filter(sub_query)

    return query


def filter_query_by_group(query, model_class):
    serializer = GroupRequestSerializer()
    args = serializer.to_value(request.args)

    # Filter by group
    if 'group' in args:
        query = query.filter(model_class.group_id == args['group'])

    return query


class GroupRequestSerializer(serializers.Serializer):
    group = fields.IntegerField(required=False)


class GroupObjectViewMixin(object):
    def get_permission_classes(self):
        permission_classes = super(GroupObjectViewMixin, self).get_permission_classes()
        permission_classes.append(GroupObjectPermission)
        return permission_classes

    def filter_query(self, query):
        query = super(GroupObjectViewMixin, self).filter_query(query)
        model_class = self.get_model_class()
        query = filter_query_by_group_permissions(query, model_class)
        query = filter_query_by_group(query, model_class)
        return query


def filter_query_by_patient_permissions(query, model_class):
    patients_query = PatientQueryBuilder(current_user).build()
    patients_query = patients_query.filter(Patient.id == model_class.patient_id)
    query = query.filter(patients_query.exists())
    return query


def filter_query_by_patient(query, model_class):
    args = parse_args(PatientRequestSerializer)

    if args['patient'] is not None:
        query = query.filter(model_class.patient_id == args['patient'])

    return query


class PatientRequestSerializer(serializers.Serializer):
    patient = fields.IntegerField(required=False)


class PatientObjectViewMixin(object):
    def get_permission_classes(self):
        permission_classes = super(PatientObjectViewMixin, self).get_permission_classes()
        permission_classes.append(PatientObjectPermission)
        return permission_classes

    def filter_query(self, query):
        query = super(PatientObjectViewMixin, self).filter_query(query)
        model_class = self.get_model_class()
        query = filter_query_by_patient_permissions(query, model_class)
        query = filter_query_by_patient(query, model_class)
        return query


class PatientObjectListView(PatientObjectViewMixin, ListCreateModelView):
    pass


class PatientObjectDetailView(PatientObjectViewMixin, RetrieveUpdateDestroyModelView):
    pass


class DemographicsViewMixin(object):
    def filter_query(self, query):
        query = super(DemographicsViewMixin, self).filter_query(query)

        if not current_user.is_admin:
            query = query.filter(filter_by_permissions(current_user, True))

        return query


class SourceRequestSerializer(serializers.Serializer):
    source_group = fields.IntegerField(required=False)
    source_type = fields.StringField(required=False)


class SourceFilterMixin(object):
    def filter_query(self, query):
        query = super(SourceFilterMixin, self).filter_query(query)

        # Note: if a user can view the patient (see PatientObjectViewMixin.filter_query) they can *view* the patient's
        # data from any data source.

        args = parse_args(SourceRequestSerializer)

        # Filter by source group
        if args['source_group'] is not None:
            model_class = self.get_model_class()
            query = query.filter(model_class.source_group_id == args['source_group'])

        # Filter by source type
        if args['source_type'] is not None:
            model_class = self.get_model_class()
            query = query.filter(model_class.source_type == args['source_type'])

        return query


class SourceObjectViewMixin(SourceFilterMixin):
    def get_permission_classes(self):
        permission_classes = super(SourceObjectViewMixin, self).get_permission_classes()
        permission_classes.append(SourceObjectPermission)
        return permission_classes


class RadarObjectViewMixin(SourceFilterMixin):
    def get_permission_classes(self):
        permission_classes = super(RadarObjectViewMixin, self).get_permission_classes()
        permission_classes.append(RadarSourceObjectPermission)
        return permission_classes


class UserRequestSerializer(serializers.Serializer):
    user = fields.IntegerField(required=False)


def filter_query_by_user_permissions(query, model_class):
    users_query = UserQueryBuilder(current_user).build()
    users_query = users_query.filter(User.id == model_class.user_id)
    query = query.filter(users_query.exists())
    return query


def filter_query_by_user(query, model_class):
    args = parse_args(UserRequestSerializer)

    if args['user'] is not None:
        query = query.filter(model_class.user_id == args['user'])

    return query

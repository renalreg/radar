from sqlalchemy import or_, and_
from sqlalchemy.orm import aliased
from flask import request

from radar.database import db
from radar.models.groups import Group, GroupPatient, GroupUser, GROUP_TYPE_COHORT, GROUP_TYPE_HOSPITAL
from radar.permissions import GroupObjectPermission
from radar.roles import get_roles_with_permission, PERMISSION
from radar.serializers.core import Serializer
from radar.serializers.fields import IntegerField
from radar.auth.sessions import current_user


def filter_query_by_group_permissions(query, model_class):
    # Filter the query based on the user's group membership
    # Admins can view all data so don't filter their queries
    if not current_user.is_admin:
        group_a = aliased(Group)
        group_b = aliased(Group)

        query = query.join(group_a, model_class.group)

        # Check if the user has permission through their group membership (requires the VIEW_PATIENT permission)
        # If the user has the VIEW_PATIENT permission on one of the patient's hospitals they can view all cohort data
        sub_query = db.session.query(GroupPatient)\
            .join(group_b, GroupPatient.group)\
            .join(Group.group_users)\
            .filter(
                GroupPatient.patient_id == model_class.patient_id,
                GroupUser.user == current_user,
                GroupUser.role.in_(get_roles_with_permission(PERMISSION.VIEW_PATIENT)),
                or_(
                    GroupPatient.group_id == model_class.group_id,
                    and_(
                        group_a.type == GROUP_TYPE_COHORT,
                        group_b.type == GROUP_TYPE_HOSPITAL
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


class GroupRequestSerializer(Serializer):
    group = IntegerField()


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

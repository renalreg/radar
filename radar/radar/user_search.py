from sqlalchemy import or_
from sqlalchemy.orm import aliased

from radar.database import db
from radar.models.groups import GroupUser, Group
from radar.models.users import User
from radar.roles import get_roles_with_permission, PERMISSIONS
from radar.permissions import has_permission_for_any_group


class UserQueryBuilder(object):
    def __init__(self, current_user):
        self.query = User.query
        self.current_user = current_user

    def user_id(self, user_id):
        self.query = self.query.filter(User.id == user_id)
        return self

    def username(self, username):
        self.query = self.query.filter(User.username.ilike('%' + username + '%'))
        return self

    def email(self, email):
        self.query = self.query.filter(User.email.ilike('%' + email + '%'))
        return self

    def first_name(self, first_name):
        self.query = self.query.filter(User.first_name.ilike(first_name + '%'))
        return self

    def last_name(self, last_name):
        self.query = self.query.filter(User.last_name.ilike(last_name + '%'))
        return self

    def group(self, group):
        sub_query = db.session.query(GroupUser)\
            .filter(
                GroupUser.group == group,
                GroupUser.user_id == User.id,
            )\
            .exists()

        # Include admins even though they don't have explicit group membership
        self.query = self.query.filter(or_(
            User.is_admin,
            sub_query
        ))

        return self

    def build(self):
        query = self.query

        # Show all users if the user is an admin or if the user can manage group membership
        all_users = (
            self.current_user.is_admin or
            has_permission_for_any_group(self.current_user, PERMISSIONS.EDIT_USER_MEMBERSHIP)
        )

        if not all_users:
            query = query.filter(filter_by_permissions(self.current_user))

        return query


def filter_by_permissions(current_user):
    # Grant access based on membership of a common group where the user has the VIEW_USER permission
    # User's can always view their own accounts
    return or_(
        filter_by_roles(current_user, get_roles_with_permission(PERMISSIONS.VIEW_USER)),
        User.id == current_user.id
    )


def filter_by_roles(current_user, roles):
    # Alias as we are joining against the GroupUser table twice
    group_user_alias = aliased(GroupUser)

    # Users in the same group as the parent user (correlated query)
    query = db.session.query(GroupUser)\
        .join(GroupUser.group)\
        .join(group_user_alias, Group.group_users)\
        .filter(GroupUser.user_id == User.id)

    # Filter on the current user's group membership and roles
    query = query.filter(
        group_user_alias.user_id == current_user.id,
        group_user_alias.role.in_(roles)
    )

    return query.exists()

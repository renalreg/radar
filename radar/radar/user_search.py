from sqlalchemy import or_
from sqlalchemy.orm import aliased

from radar.database import db
from radar.models import OrganisationUser, Organisation, CohortUser
from radar.models.cohorts import Cohort
from radar.models.users import User
from radar.roles import get_cohort_roles_with_permission, get_organisation_roles_with_permission, PERMISSIONS
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

    def organisation(self, organisation):
        # Show users that have access to an organisation
        # Include admins even though they don't have explicit membership
        self.query = self.query\
            .outerjoin(User.organisation_users)\
            .filter(or_(User.is_admin, OrganisationUser.organisation == organisation))

    def cohort(self, cohort):
        # Show users that have access to a cohort
        # Include admins even though they don't have explicit membership
        self.query = self.query\
            .outerjoin(User.cohort_users)\
            .filter(or_(User.is_admin, CohortUser.cohort == cohort))

    def build(self):
        query = self.query

        # Show all users if the user is an admin or if the user can manage group membership
        all_users = (
            self.current_user.is_admin or
            has_permission_for_any_group(self.current_user, 'has_edit_user_membership_permission')  # TODO
        )

        if not all_users:
            query = query.filter(filter_by_permissions(self.current_user))

        return query


def filter_by_permissions(current_user):
    # Grant access based on membership of a common organisation/cohort where the user has the view user permission
    # User's can always view their own accounts
    return or_(
        filter_by_organisation_roles(current_user, get_organisation_roles_with_permission(PERMISSIONS.VIEW_USER)),
        filter_by_cohort_roles(current_user, get_cohort_roles_with_permission(PERMISSIONS.VIEW_USER)),
        User.id == current_user.id
    )


def filter_by_organisation_roles(current_user, roles):
    # Alias as we are joining against the OrganisationUser table twice
    organisation_user_alias = aliased(OrganisationUser)

    # Users in the same organisation as the parent user (correlated query)
    query = db.session.query(OrganisationUser)\
        .join(OrganisationUser.organisation)\
        .join(organisation_user_alias, Organisation.organisation_users)\
        .filter(OrganisationUser.user_id == User.id)

    # Filter on the current user's organisation membership and roles
    query = query.filter(
        organisation_user_alias.user_id == current_user.id,
        organisation_user_alias.role.in_(roles)
    )

    return query.exists()


def filter_by_cohort_roles(current_user, roles):
    # Alias as we are joining against the CohortUser table twice
    cohort_user_alias = aliased(CohortUser)

    # Users in the same cohort as the parent user (correlated query)
    query = db.session.query(CohortUser)\
        .join(CohortUser.cohort)\
        .join(cohort_user_alias, Cohort.cohort_users)\
        .filter(CohortUser.user_id == User.id)

    # Filter on the current user's cohort membership and roles
    query = query.filter(
        cohort_user_alias.user_id == current_user.id,
        cohort_user_alias.role.in_(roles)
    )

    return query.exists()

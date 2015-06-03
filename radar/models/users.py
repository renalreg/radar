from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from radar.models.common import ModifiedMixin, CreatedMixin
from radar.lib.roles import UNIT_ROLES, DISEASE_GROUP_ROLES, DISEASE_GROUP_MANAGED_ROLES, UNIT_MANAGED_ROLES
from radar.lib.database import db


class UserCreatedMixin(CreatedMixin):
    @declared_attr
    def created_user(cls):
        return relationship('User', foreign_keys=[cls.created_user_id], remote_side='User.id', post_update=True)


class UserModifiedMixin(ModifiedMixin):
    @declared_attr
    def modified_user(cls):
        return relationship('User', foreign_keys=[cls.modified_user_id], remote_side='User.id', post_update=True)


class User(db.Model, UserCreatedMixin, UserModifiedMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    email = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    is_admin = Column(Boolean, default=False, nullable=False, server_default='0')

    reset_password_token = Column(String)
    reset_password_date = Column(DateTime)

    force_password_change = Column(Boolean, default=False, nullable=False, server_default='0')

    unit_users = relationship('UnitUser', back_populates='user')
    disease_group_users = relationship('DiseaseGroupUser', back_populates='user')

    @property
    def units(self):
        return [x.unit for x in self.unit_users]

    @property
    def disease_groups(self):
        return [x.disease_group for x in self.disease_group_users]

    @property
    def facilities(self):
        facilities = []

        for x in self.units:
            facilities.extend(x.facilities)

        return facilities

    @property
    def internal_facilities(self):
        facilities = []

        for x in self.units:
            facilities.extend(x.internal_facilities)

        return facilities

    @property
    def edit_patient_facilities(self):
        facilities = []

        for x in self.unit_users:
            if x.unit.has_edit_patient_permission:
                facilities.extend(x.unit.internal_facilities)

        return facilities

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.reset_password_token = None
        self.force_password_change = False

    def set_initial_password(self, password):
        self.set_password(password)
        self.force_password_change = True

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @property
    def has_view_patient_permission(self):
        return (
            self.is_admin or
            any(x.has_view_patient_permission for x in self.disease_group_users) or
            any(x.has_view_patient_permission for x in self.unit_users)
        )

    @property
    def has_recruit_patient_permission(self):
        return (
            self.is_admin or
            any(x.has_recruit_patient_permission for x in self.unit_users)
        )

    @property
    def has_view_demographics_permission(self):
        return (
            self.is_admin or
            any(x.has_demographics_permission for x in self.disease_group_users) or
            any(x.has_demographics_permission for x in self.unit_users)
        )

    @property
    def has_view_user_permission(self):
        return (
            self.is_admin or
            any(x.has_view_user_permission for x in self.disease_group_users) or
            any(x.has_view_user_permission for x in self.unit_users)
        )

    @property
    def has_add_user_permission(self):
        return (
            self.is_admin or
            self.has_edit_user_membership_permission
        )

    @property
    def has_edit_user_membership_permission(self):
        return (
            self.is_admin or
            any(x.has_edit_user_membership_permission for x in self.disease_group_users) or
            any(x.has_edit_user_membership_permission for x in self.unit_users)
        )

    @property
    def has_edit_news_permission(self):
        return self.is_admin

    def filter_units_for_user(self, current_user):
        # TODO
        return self.units

    def filter_disease_groups_for_user(self, current_user):
        # TODO
        return self.disease_groups

    def can_view(self, user):
        # TODO
        return True

    def _get_managed_roles(self, all_roles, managed_role_map, group_users):
        if self.is_admin:
            return all_roles

        # Disease group roles user can manage
        managed_roles = set()

        # Build list of roles
        for group_user in group_users:
            managed_roles |= managed_role_map.get(group_user.role, list)

        # Return roles ordered by access level
        return [x for x in all_roles if x in managed_roles]

    @property
    def managed_unit_roles(self):
        return self._get_managed_roles(UNIT_ROLES, UNIT_MANAGED_ROLES, self.unit_users)

    @property
    def managed_disease_group_roles(self):
        return self._get_managed_roles(DISEASE_GROUP_ROLES, DISEASE_GROUP_MANAGED_ROLES, self.disease_group_users)

    def _can_edit_roles(self, current_user):
        # User's can't edit their own roles (unless they are an admin)
        # This is to stop user's locking themselves out
        if self == current_user and not current_user.is_admin:
            return False

        # Can't edit an admin's roles (unless it is you)
        if self.is_admin and self != current_user:
            return False

        return True

    def can_edit_disease_group_roles(self, current_user):
        if not self._can_edit_roles(current_user):
            return False

        if len(current_user.managed_disease_group_roles) == 0:
            return False

        return True

    def can_edit_unit_roles(self, current_user):
        if not self._can_edit_roles(current_user):
            return False

        if len(current_user.managed_unit_roles) == 0:
            return False

        return True

    def __str__(self):
        if self.first_name and self.last_name:
            return '%s %s (%s)' % (self.first_name, self.last_name, self.email)
        else:
            return '%s (%s)' % (self.username, self.email)

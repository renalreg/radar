from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from radar.models import CreatedModifiedMixin, ModifiedMixin, CreatedMixin
from radar.users.roles import DISEASE_GROUP_VIEW_PATIENT_ROLES, \
    DISEASE_GROUP_VIEW_DEMOGRAPHICS_ROLES, UNIT_VIEW_DEMOGRAPHICS_ROLES, UNIT_VIEW_PATIENT_ROLES, \
    DISEASE_GROUP_VIEW_USER_ROLES, UNIT_VIEW_USER_ROLES, UNIT_EDIT_PATIENT_ROLES, DISEASE_GROUP_ROLE_NAMES, \
    UNIT_ROLE_NAMES, UNIT_ROLES, DISEASE_GROUP_ROLES, DISEASE_GROUP_MANAGED_ROLES, UNIT_MANAGED_ROLES, \
    UNIT_RECRUIT_PATIENT_ROLES
from radar.database import db


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
    is_admin = Column(Boolean, default=False, nullable=False)

    reset_password_token = Column(String)
    reset_password_date = Column(DateTime)

    force_password_change = Column(Boolean, default=False, nullable=False)

    units = relationship('UnitUser', back_populates='user')
    disease_groups = relationship('DiseaseGroupUser', back_populates='user')

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
            any(x.has_view_patient_permission for x in self.disease_groups) or
            any(x.has_view_patient_permission for x in self.units)
        )

    @property
    def has_recruit_patient_permission(self):
        return (
            self.is_admin or
            any(x.has_recruit_patient_permission for x in self.units)
        )

    @property
    def has_view_demographics_permission(self):
        return (
            self.is_admin or
            any(x.has_demographics_permission for x in self.disease_groups) or
            any(x.has_demographics_permission for x in self.units)
        )

    @property
    def has_view_user_permission(self):
        return (
            self.is_admin or
            any(x.has_view_user_permission for x in self.disease_groups) or
            any(x.has_view_user_permission for x in self.units)
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
            any(x.has_edit_user_membership_permission for x in self.disease_groups) or
            any(x.has_edit_user_membership_permission for x in self.units)
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
        return self._get_managed_roles(UNIT_ROLES, UNIT_MANAGED_ROLES, self.units)

    @property
    def managed_disease_group_roles(self):
        return self._get_managed_roles(DISEASE_GROUP_ROLES, DISEASE_GROUP_MANAGED_ROLES, self.disease_groups)

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


class DiseaseGroupUser(db.Model):
    __tablename__ = 'disease_group_users'

    id = Column(Integer, primary_key=True)
    disease_group_id = Column(Integer, ForeignKey('disease_groups.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role = Column(String, nullable=False)

    user = relationship('User')
    disease_group = relationship('DiseaseGroup')

    __table_args__ = (
        UniqueConstraint('disease_group_id', 'user_id'),
    )

    @hybrid_property
    def has_view_demographics_permission(self):
        return self.role in DISEASE_GROUP_VIEW_DEMOGRAPHICS_ROLES

    @hybrid_property
    def has_view_patient_permission(self):
        return self.role in DISEASE_GROUP_VIEW_PATIENT_ROLES

    @hybrid_property
    def has_view_user_permission(self):
        return self.role in DISEASE_GROUP_VIEW_USER_ROLES

    @property
    def has_edit_user_membership_permission(self):
        managed_roles = DISEASE_GROUP_MANAGED_ROLES.get(self.role)
        return managed_roles is not None and len(managed_roles) > 0

    def can_edit(self, user):
        # TODO
        return True

    @property
    def role_name(self):
        return DISEASE_GROUP_ROLE_NAMES.get(self.role)


class UnitUser(db.Model):
    __tablename__ = 'unit_users'

    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, ForeignKey('units.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role = Column(String, nullable=False)

    unit = relationship('Unit')
    user = relationship('User')

    __table_args__ = (
        UniqueConstraint('unit_id', 'user_id'),
    )

    @hybrid_property
    def has_view_demographics_permission(self):
        return self.role in UNIT_VIEW_DEMOGRAPHICS_ROLES

    @hybrid_property
    def has_view_patient_permission(self):
        return self.role in UNIT_VIEW_PATIENT_ROLES

    @hybrid_property
    def has_edit_patient_permission(self):
        return self.role in UNIT_EDIT_PATIENT_ROLES

    @hybrid_property
    def has_view_user_permission(self):
        return self.role in UNIT_VIEW_USER_ROLES

    @property
    def has_edit_user_membership_permission(self):
        managed_roles = UNIT_MANAGED_ROLES.get(self.role)
        return managed_roles is not None and len(managed_roles) > 0

    @hybrid_property
    def has_recruit_patient_permission(self):
        return self.role in UNIT_RECRUIT_PATIENT_ROLES

    @property
    def role_name(self):
        return UNIT_ROLE_NAMES.get(self.role)

    def can_edit(self, user):
        # TODO
        return True
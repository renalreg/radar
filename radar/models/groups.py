from datetime import datetime
from enum import Enum

import pytz
from sqlalchemy import (
    and_,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    func,
    Index,
    Integer,
    null,
    or_,
    String,
    text,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, relationship, synonym

from radar.config import config
from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship
from radar.models.logs import log_changes
from radar.models.types import EnumToStringType, EnumType
from radar.pages import PAGE
from radar.roles import get_roles_managed_by_role, get_roles_with_permission, PERMISSION, ROLE


class GROUP_TYPE(Enum):
    HOSPITAL = 'HOSPITAL'
    COHORT = 'COHORT'
    SYSTEM = 'SYSTEM'
    OTHER = 'OTHER'

    def __str__(self):
        return str(self.value)


GROUP_CODE_UKRDC = 'UKRDC'
GROUP_CODE_UKRR = 'UKRR'
GROUP_CODE_RADAR = 'RADAR'
GROUP_CODE_NHS = 'NHS'
GROUP_CODE_CHI = 'CHI'
GROUP_CODE_HSC = 'HSC'
GROUP_CODE_NHSBT = 'NHSBT'
GROUP_CODE_BAPN = 'BAPN'
GROUP_CODE_NURTURE = 'NURTURE'


@log_changes
class Group(db.Model):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    type = Column(EnumType(GROUP_TYPE, name='group_type'), nullable=False)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)

    # Parent group is required for cohort groups (should be a system group). It should be
    # null for other types of group.
    parent_group_id = Column(Integer, ForeignKey('groups.id'), CheckConstraint("""
        (type != 'COHORT' and parent_group_id is null) or
        (type = 'COHORT' and parent_group_id is not null)
    """))
    parent_group = relationship('Group', remote_side=[id])

    _instructions = Column('instructions', String)
    multiple_diagnoses = Column(Boolean, nullable=False, default=False, server_default=text('false'))
    is_recruitment_number_group = Column(Boolean, nullable=False, default=False, server_default=text('false'))
    is_transplant_centre = Column(Boolean, nullable=True, default=False, server_default=text('false'))
    country_code = Column(String, ForeignKey('countries.code'), nullable=True)
    country = relationship('Country', foreign_keys=[country_code], backref=backref('groups'))

    @property
    def patients(self):
        return [x.patient for x in self.group_patient]

    @property
    def users(self):
        return [x.user for x in self.group_users]

    @property
    def has_dependencies(self):
        """Returns true if this group has a dependency on another group."""

        try:
            check_dependencies([self])
        except DependencyError:
            return True
        else:
            return False

    @property
    def instructions(self):
        if self._instructions is not None:
            return self._instructions
        elif self.type == GROUP_TYPE.COHORT:
            return config.get('DEFAULT_INSTRUCTIONS')
        else:
            return None

    @instructions.setter
    def instructions(self, value):
        self._instructions = value

    instructions = synonym('_instructions', descriptor=instructions)

    def __unicode__(self):
        return self.name

Index('groups_code_type_idx', Group.code, Group.type, unique=True)


@log_changes
class GroupPatient(db.Model, MetaModelMixin):
    __tablename__ = 'group_patients'

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship(
        'Group',
        foreign_keys=[group_id],
        backref=backref('group_patients', cascade='all, delete-orphan', passive_deletes=True))

    patient_id = patient_id_column()
    patient = patient_relationship('group_patients')

    from_date = Column(DateTime(timezone=True), nullable=False)
    to_date = Column(DateTime(timezone=True))

    created_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    created_group = relationship('Group', foreign_keys=[created_group_id])

    @hybrid_property
    def current(self):
        """Returns true if today's date is between the from and to date."""

        now = datetime.now(pytz.UTC)
        return (self.from_date <= now and (self.to_date is None or self.to_date >= now))

    @current.expression
    def current(cls):
        return and_(cls.from_date <= func.now(), or_(cls.to_date == null(), cls.to_date >= func.now()))

Index('group_patients_group_idx', GroupPatient.group_id)
Index('group_patients_patient_idx', GroupPatient.patient_id)


@log_changes
class GroupUser(db.Model, MetaModelMixin):
    __tablename__ = 'group_users'

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship('Group', backref=backref('group_users', cascade='all, delete-orphan', passive_deletes=True))

    user_id = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    user = relationship(
        'User',
        foreign_keys=[user_id],
        backref=backref('group_users', cascade='all, delete-orphan', passive_deletes=True))
    role = Column(EnumType(ROLE, name='role'), nullable=False)

    def has_permission(self, permission):
        permission_method = permission.value.lower()
        grant = getattr(self, 'has_' + permission_method + '_permission', None)

        if grant is None:
            roles = get_roles_with_permission(permission)
            grant = self.role in roles

        return grant

    @property
    def permissions(self):
        return [x for x in PERMISSION if self.has_permission(x)]

    @property
    def has_edit_user_membership_permission(self):
        return len(self.managed_roles) > 0

    @property
    def managed_roles(self):
        return get_roles_managed_by_role(self.role)


Index('group_users_group_idx', GroupUser.group_id)
Index('group_users_user_idx', GroupUser.user_id)
Index('group_patients_group_user_role_idx', GroupUser.group_id, GroupUser.user_id, GroupUser.role, unique=True)


@log_changes
class GroupPage(db.Model):
    __tablename__ = 'group_pages'

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey('groups.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    group = relationship('Group', backref=backref('group_pages', cascade='all, delete-orphan', passive_deletes=True))

    page = Column(EnumToStringType(PAGE), nullable=False)

    weight = Column(Integer, CheckConstraint('weight >= 0'), nullable=False)

Index('group_pages_group_idx', GroupPage.group_id)
Index('group_pages_page_idx', GroupPage.page)
Index('group_pages_page_group_idx', GroupPage.page, GroupPage.group_id, unique=True)


dependencies = [
    ((GROUP_TYPE.COHORT, 'NEPHROS'), (GROUP_TYPE.COHORT, 'INS')),
    ((GROUP_TYPE.COHORT, 'NSMPGNC3'), (GROUP_TYPE.COHORT, 'MPGN')),
]


class DependencyError(Exception):
    pass


def check_dependencies(groups):
    """Check group dependencies (e.g. if in x, must be in y)."""

    groups = set((group.type, group.code) for group in groups)

    for x, y in dependencies:
        if x in groups and y not in groups:
            raise DependencyError('Must be in {0}.'.format(y[1]))

from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Index, DateTime, and_, or_, func, null
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.hybrid import hybrid_property
import pytz

from radar.database import db
from radar.roles import ROLE, PERMISSION, get_roles_with_permission, get_roles_managed_by_role
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship
from radar.pages import PAGE
from radar.models.types import EnumType, EnumToStringType

# TODO enum
GROUP_TYPE_HOSPITAL = 'HOSPITAL'
GROUP_TYPE_COHORT = 'COHORT'
GROUP_TYPE_OTHER = 'OTHER'

GROUP_CODE_UKRDC = 'UKRDC'
GROUP_CODE_UKRR = 'UKRR'
GROUP_CODE_RADAR = 'RADAR'
GROUP_CODE_NHS = 'NHS'
GROUP_CODE_CHI = 'CHI'
GROUP_CODE_HANDC = 'HANDC'
GROUP_CODE_NHSBT = 'NHSBT'
GROUP_CODE_BAPN = 'BAPN'


class Group(db.Model):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)

    # https://bitbucket.org/zzzeek/sqlalchemy/issues/3467/array-of-enums-does-not-allow-assigning
    pages = Column('pages', postgresql.ARRAY(EnumToStringType(PAGE)))

    notes = Column(String)

    @property
    def patients(self):
        return [x.patient for x in self.group_patient]

    @property
    def users(self):
        return [x.user for x in self.group_users]

    @property
    def sorted_pages(self):
        return [x.name for x in sorted(self.group_pages, key=lambda y: y.display_order)]

Index('groups_code_type_idx', Group.code, Group.type, unique=True)


class GroupPatient(db.Model, MetaModelMixin):
    __tablename__ = 'group_patients'

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    group = relationship('Group', foreign_keys=[group_id], backref=backref('group_patients', cascade='all, delete-orphan', passive_deletes=True))

    patient_id = patient_id_column()
    patient = patient_relationship('group_patients')

    from_date = Column(DateTime(timezone=True), nullable=False)
    to_date = Column(DateTime(timezone=True))

    created_group_id = Column(Integer, ForeignKey('groups.id'))
    created_group = relationship('Group', foreign_keys=[created_group_id])

    @hybrid_property
    def current(self):
        now = datetime.now(pytz.UTC)
        return (self.from_date <= now and (self.to_date is None or self.to_date >= now))

    @current.expression
    def current(cls):
        return and_(cls.from_date <= func.now(), or_(cls.to_date == null(), cls.to_date >= func.now()))

Index('group_patients_group_idx', GroupPatient.group_id)
Index('group_patients_patient_idx', GroupPatient.patient_id)


class GroupUser(db.Model, MetaModelMixin):
    __tablename__ = 'group_users'

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship('Group', backref=backref('group_users', cascade='all, delete-orphan', passive_deletes=True))

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', foreign_keys=[user_id])
    role = Column('role', EnumType(ROLE, name='role'), nullable=False)

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
Index('group_patients_group_user_idx', GroupUser.group_id, GroupUser.user_id, unique=True)

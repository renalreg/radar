from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index, DateTime
from sqlalchemy.orm import relationship, backref

from radar.database import db
from radar.roles import ROLES, PERMISSIONS, get_roles_with_permission, get_managed_roles_for_role
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship
from radar.pages import PAGES

GROUP_TYPE_HOSPITAL = 'HOSPITAL'
GROUP_TYPE_COHORT = 'COHORT'
GROUP_TYPE_OTHER = 'OTHER'

GROUP_TYES = [
    GROUP_TYPE_HOSPITAL,
    GROUP_TYPE_COHORT,
    GROUP_TYPE_OTHER,
]

OTHER_UKRDC = 'UKRDC'
OTHER_UKRR = 'UKRR'
OTHER_RADAR = 'RADAR'
OTHER_NHS = 'NHS'
OTHER_CHI = 'CHI'
OTHER_HANDC = 'HANDC'
OTHER_NHSBT = 'NHSBT'
OTHER_BAPN = 'BAPN'


class Group(db.Model):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    notes = Column(String)

    group_patients = relationship('GroupPatient')
    group_users = relationship('GroupUser')
    group_pages = relationship('GroupPage')

    # TODO recruitment

    @property
    def patients(self):
        return [x.patient for x in self.group_patient]

    @property
    def users(self):
        return [x.user for x in self.group_users]

    @property
    def sorted_pages(self):
        return [x.name for x in sorted(self.group_pages, key=lambda y: y.display_order)]


class GroupPatient(db.Model, MetaModelMixin):
    __tablename__ = 'group_patients'

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    group = relationship('Group')

    patient_id = patient_id_column()
    patient = patient_relationship('group_patients')

    from_date = Column(DateTime(timezone=True), nullable=False)
    to_date = Column(DateTime(timezone=True))

    created_group_id = Column(Integer, ForeignKey('groups.id'))
    created_group = relationship('Group')

    __table_args__ = (
        UniqueConstraint('group_id', 'patient_id'),
    )

Index('group_patients_group_id_idx', GroupPatient.group_id)
Index('group_patients_patient_id_idx', GroupPatient.patient_id)


class GroupUser(db.Model, MetaModelMixin):
    __tablename__ = 'group_users'

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship('Group')

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', foreign_keys=[user_id])

    _role = Column('role', String, nullable=False)

    __table_args__ = (
        UniqueConstraint('group_id', 'user_id'),
    )

    @property
    def role(self):
        value = self._role

        if value is not None:
            value = ROLES(value)

        return value

    @role.setter
    def role(self, value):
        if value is not None:
            value = value.value

        self._role = value

    def has_permission(self, permission):
        permission_method = permission.value.lower()
        grant = getattr(self, 'has_' + permission_method + '_permission', None)

        if grant is None:
            roles = get_roles_with_permission(permission)
            grant = self.role in roles

        return grant

    @property
    def permissions(self):
        return [x for x in PERMISSIONS if self.has_permission(x)]

    @property
    def has_edit_user_membership_permission(self):
        return len(self.managed_roles) > 0

    @property
    def managed_roles(self):
        return get_managed_roles_for_role(self.role)

Index('group_users_group_id_idx', GroupUser.group_id)
Index('group_users_patient_id_idx', GroupUser.patient_id)


class GroupPage(db.Model):
    __tablename__ = 'group_pages'

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship('Group')

    _name = Column('name', String, nullable=False)
    display_order = Column(Integer, nullable=False)

    @property
    def name(self):
        value = self._name

        if value is not None:
            value = PAGES(value)

        return value

    @name.setter
    def name(self, value):
        if value is not None:
            value = value.value

        self._name = value

Index('group_pages_group_id_idx', GroupPage.group_id)


class GroupConsultant(db.Model, MetaModelMixin):
    __tablename__ = 'group_consultants'

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship('Group')

    consultant_id = Column(Integer, ForeignKey('consultants.id'), nullable=False)
    consultant = relationship('Consultant', backref=backref('group_consultants', cascade='all, delete-orphan', passive_deletes=True))

Index(
    'group_consultants_group_id_consultant_id_idx',
    GroupConsultant.group_id,
    GroupConsultant.consultant_id,
    unique=True
)

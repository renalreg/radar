from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint, Index
from sqlalchemy.orm import relationship, backref

from radar.database import db
from radar.roles import ORGANISATION_PERMISSIONS, ORGANISATION_MANAGED_ROLES, PERMISSIONS, ORGANISATION_ROLES
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship


ORGANISATION_CODE_UKRDC = 'UKRDC'
ORGANISATION_CODE_UKRR = 'UKRR'
ORGANISATION_CODE_RADAR = 'RADAR'
ORGANISATION_CODE_NHS = 'NHS'
ORGANISATION_CODE_CHI = 'CHI'
ORGANISATION_CODE_HANDC = 'H&C'
ORGANISATION_CODE_NHSBT = 'NHS Blood and Transplant'
ORGANISATION_CODE_BAPN = 'BAPN'

ORGANISATION_TYPE_UNIT = 'UNIT'
ORGANISATION_TYPE_OTHER = 'OTHER'

ORGANISATION_TYPES = [
    ORGANISATION_TYPE_UNIT,
    ORGANISATION_TYPE_OTHER
]


class OrganisationPatient(db.Model, MetaModelMixin):
    __tablename__ = 'organisation_patients'

    id = Column(Integer, primary_key=True)

    organisation_id = Column(Integer, ForeignKey('organisations.id'), nullable=False)
    organisation = relationship('Organisation')

    patient_id = patient_id_column()
    patient = patient_relationship('organisation_patients')

    is_active = Column(Boolean, nullable=False, default=True, server_default='true')

    __table_args__ = (
        UniqueConstraint('organisation_id', 'patient_id'),
    )

Index('organisation_patients_organisation_id_idx', OrganisationPatient.organisation_id)
Index('organisation_patients_patient_id_idx', OrganisationPatient.patient_id)


class OrganisationUser(db.Model, MetaModelMixin):
    __tablename__ = 'organisation_users'

    id = Column(Integer, primary_key=True)

    organisation_id = Column(Integer, ForeignKey('organisations.id'), nullable=False)
    organisation = relationship('Organisation')

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', foreign_keys=[user_id])

    _role = Column('role', String, nullable=False)

    @property
    def role(self):
        value = self._role

        if value is not None:
            value = ORGANISATION_ROLES(value)

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
            roles = ORGANISATION_PERMISSIONS.get(permission, [])
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
        return ORGANISATION_MANAGED_ROLES.get(self.role, [])

Index(
    'organisation_users_organisation_id_user_id_idx',
    OrganisationUser.organisation_id,
    OrganisationUser.user_id,
    unique=True
)
Index('organisation_users_organisation_id_idx', OrganisationUser.organisation_id)
Index('organisation_users_user_id_idx', OrganisationUser.user_id)


class Organisation(db.Model):
    __tablename__ = 'organisations'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)

    recruitment = Column(Boolean, nullable=False, default=False, server_default='false')

    data_sources = relationship('DataSource')
    organisation_patients = relationship('OrganisationPatient')
    organisation_users = relationship('OrganisationUser')

Index('organisations_type_code_idx', Organisation.type, Organisation.code, unique=True)
Index('organisations_code_idx', Organisation.code)
Index('organisations_type_idx', Organisation.type)


class OrganisationConsultant(db.Model, MetaModelMixin):
    __tablename__ = 'organisation_consultants'

    id = Column(Integer, primary_key=True)

    organisation_id = Column(Integer, ForeignKey('organisations.id'), nullable=False)
    organisation = relationship('Organisation')

    consultant_id = Column(Integer, ForeignKey('consultants.id'), nullable=False)
    consultant = relationship('Consultant', backref=backref('organisation_consultants', cascade='all, delete-orphan', passive_deletes=True))

Index(
    'organisation_consultants_organisation_id_consultant_id_idx',
    OrganisationConsultant.organisation_id,
    OrganisationConsultant.consultant_id,
    unique=True
)

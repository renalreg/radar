from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint, Index
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import relationship

from radar.database import db
from radar.roles import ORGANISATION_VIEW_DEMOGRAPHICS_ROLES, ORGANISATION_VIEW_PATIENT_ROLES, ORGANISATION_EDIT_PATIENT_ROLES, \
    ORGANISATION_VIEW_USER_ROLES, ORGANISATION_MANAGED_ROLES, ORGANISATION_RECRUIT_PATIENT_ROLES
from radar.models.common import MetaModelMixin


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

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    is_active = Column(Boolean, nullable=False, default=True, server_default='1')

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

    role = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('organisation_id', 'user_id'),
    )

    @hybrid_method
    def has_permission(self, permission):
        # TODO
        raise NotImplementedError()

    @hybrid_property
    def has_view_demographics_permission(self):
        return self.role in ORGANISATION_VIEW_DEMOGRAPHICS_ROLES

    @hybrid_property
    def has_view_patient_permission(self):
        return self.role in ORGANISATION_VIEW_PATIENT_ROLES

    @hybrid_property
    def has_edit_patient_permission(self):
        return self.role in ORGANISATION_EDIT_PATIENT_ROLES

    @hybrid_property
    def has_recruit_patient_permission(self):
        return self.role in ORGANISATION_RECRUIT_PATIENT_ROLES

    @hybrid_property
    def has_view_user_permission(self):
        return self.role in ORGANISATION_VIEW_USER_ROLES

    @property
    def has_edit_user_membership_permission(self):
        return len(self.managed_roles) > 0

    @property
    def managed_roles(self):
        return ORGANISATION_MANAGED_ROLES.get(self.role, [])

Index('organisation_users_organisation_id_idx', OrganisationUser.organisation_id)
Index('organisation_users_user_id_idx', OrganisationUser.user_id)


class Organisation(db.Model):
    __tablename__ = 'organisations'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)

    data_sources = relationship('DataSource')
    organisation_patients = relationship('OrganisationPatient')
    organisation_users = relationship('OrganisationUser')

    __table_args__ = (
        UniqueConstraint('type', 'code'),
    )

Index('organisations_code_idx', Organisation.code)
Index('organisations_type_idx', Organisation.type)


class OrganisationConsultant(db.Model, MetaModelMixin):
    __tablename__ = 'organisation_consultants'

    id = Column(Integer, primary_key=True)

    organisation_id = Column(Integer, ForeignKey('organisations.id'), nullable=False)
    organisation = relationship('Organisation')

    consultant_id = Column(Integer, ForeignKey('consultants.id'), nullable=False)
    consultant = relationship('Consultant')

    __table_args__ = (
        UniqueConstraint('organisation_id', 'consultant_id'),
    )

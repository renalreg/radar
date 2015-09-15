from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.lib.roles import ORGANISATION_VIEW_DEMOGRAPHICS_ROLES, ORGANISATION_VIEW_PATIENT_ROLES, ORGANISATION_EDIT_PATIENT_ROLES, \
    ORGANISATION_VIEW_USER_ROLES, ORGANISATION_MANAGED_ROLES, ORGANISATION_RECRUIT_PATIENT_ROLES
from radar.lib.models.common import MetaModelMixin

ORGANISATION_CODE_UKRR = 'UKRR'
ORGANISATION_CODE_RADAR = 'RADAR'
ORGANISATION_CODE_NHS = 'NHS'
ORGANISATION_CODE_CHI = 'CHI'
ORGANISATION_CODE_HANDC = 'H&C'

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
    def has_view_user_permission(self):
        return self.role in ORGANISATION_VIEW_USER_ROLES

    @property
    def has_edit_user_membership_permission(self):
        managed_roles = ORGANISATION_MANAGED_ROLES.get(self.role)
        return managed_roles is not None and len(managed_roles) > 0

    @hybrid_property
    def has_recruit_patient_permission(self):
        return self.role in ORGANISATION_RECRUIT_PATIENT_ROLES


class Organisation(db.Model, MetaModelMixin):
    __tablename__ = 'organisations'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)

    data_sources = relationship('DataSource')
    organisation_patients = relationship('OrganisationPatient')
    organisation_users = relationship('OrganisationUser', foreign_keys=[OrganisationUser.organisation_id])

    __table_args__ = (
        UniqueConstraint('type', 'code'),
    )

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.lib.roles import UNIT_VIEW_DEMOGRAPHICS_ROLES, UNIT_VIEW_PATIENT_ROLES, UNIT_EDIT_PATIENT_ROLES, \
    UNIT_VIEW_USER_ROLES, UNIT_MANAGED_ROLES, UNIT_RECRUIT_PATIENT_ROLES, UNIT_ROLE_NAMES
from radar.models.common import MetadataMixin


class Unit(db.Model):
    __tablename__ = 'units'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    facilities = relationship('Facility')
    unit_patients = relationship('UnitPatient')
    unit_users = relationship('UnitUser')

    @property
    def internal_facilities(self):
        return [x for x in self.facilities if x.is_internal]


class UnitPatient(db.Model, MetadataMixin):
    __tablename__ = 'unit_patients'

    id = Column(Integer, primary_key=True)

    unit_id = Column(Integer, ForeignKey('units.id'), nullable=False)
    unit = relationship('Unit')

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    is_active = Column(Boolean, nullable=False, default=True, server_default='1')

    __table_args__ = (
        UniqueConstraint('unit_id', 'patient_id'),
    )

    def can_edit(self, current_user):
        # TODO
        return True


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

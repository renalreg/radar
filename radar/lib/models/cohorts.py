from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.lib.roles import COHORT_VIEW_DEMOGRAPHICS_ROLES, COHORT_VIEW_PATIENT_ROLES, \
    COHORT_VIEW_USER_ROLES, COHORT_MANAGED_ROLES
from radar.lib.models.common import MetaModelMixin


class Cohort(db.Model, MetaModelMixin):
    __tablename__ = 'cohorts'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    cohort_patients = relationship('CohortPatient')
    cohort_users = relationship('CohortUser')
    cohort_features = relationship('CohortFeature')
    cohort_result_group_definitions = relationship('CohortResultGroupDefinition')

    notes = Column(String)

    @property
    def patients(self):
        return [x.patient for x in self.cohort_patients]

    @property
    def users(self):
        return [x.user for x in self.cohort_users]


class CohortFeature(db.Model):
    __tablename__ = 'cohort_features'

    id = Column(Integer, primary_key=True)

    cohort_id = Column(Integer, ForeignKey('cohorts.id'))
    cohort = relationship('Cohort')

    name = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)


class CohortPatient(db.Model, MetaModelMixin):
    __tablename__ = 'cohort_patients'

    id = Column(Integer, primary_key=True)

    cohort_id = Column(Integer, ForeignKey('cohorts.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    cohort = relationship('Cohort')

    patient_id = Column(Integer, ForeignKey('patients.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    patient = relationship('Patient')

    is_active = Column(Boolean, nullable=False, default=True, server_default='1')

    __table_args__ = (
        UniqueConstraint('cohort_id', 'patient_id'),
    )


class CohortUser(db.Model, MetaModelMixin):
    __tablename__ = 'cohort_users'

    id = Column(Integer, primary_key=True)

    cohort_id = Column(Integer, ForeignKey('cohorts.id'), nullable=False)
    cohort = relationship('Cohort')

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', foreign_keys=[user_id])

    role = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('cohort_id', 'user_id'),
    )

    @hybrid_property
    def has_view_demographics_permission(self):
        return self.role in COHORT_VIEW_DEMOGRAPHICS_ROLES

    @hybrid_property
    def has_view_patient_permission(self):
        return self.role in COHORT_VIEW_PATIENT_ROLES

    @hybrid_property
    def has_view_user_permission(self):
        return self.role in COHORT_VIEW_USER_ROLES

    @property
    def has_edit_user_membership_permission(self):
        return len(self.managed_roles) > 0

    @property
    def managed_roles(self):
        return COHORT_MANAGED_ROLES.get(self.role, [])


class CohortResultGroupDefinition(db.Model):
    __tablename__ = 'cohort_result_group_definitions'

    id = Column(Integer, primary_key=True)

    cohort_id = Column(Integer, ForeignKey('cohorts.id'), nullable=False)
    cohort = relationship('Cohort')

    result_group_definition_id = Column(Integer, ForeignKey('result_group_definitions.id'), nullable=False)
    result_group_definition = relationship('ResultGroupDefinition')

    weight = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('cohort_id', 'result_group_definition_id'),
    )

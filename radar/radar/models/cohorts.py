from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint, Index
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import relationship

from radar.database import db
from radar.roles import COHORT_VIEW_DEMOGRAPHICS_ROLES, COHORT_VIEW_PATIENT_ROLES, \
    COHORT_VIEW_USER_ROLES, COHORT_MANAGED_ROLES
from radar.models.common import MetaModelMixin


class Cohort(db.Model):
    __tablename__ = 'cohorts'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    notes = Column(String)

    cohort_patients = relationship('CohortPatient')
    cohort_users = relationship('CohortUser')
    cohort_features = relationship('CohortFeature')
    cohort_result_group_specs = relationship('CohortResultGroupSpec')

    @property
    def patients(self):
        return [x.patient for x in self.cohort_patients]

    @property
    def users(self):
        return [x.user for x in self.cohort_users]

    @property
    def sorted_result_groups(self):
        return [x.result_group_spec for x in sorted(self.cohort_result_group_specs, key=lambda y: y.weight)]

    @property
    def sorted_features(self):
        return [x.name for x in sorted(self.cohort_features, key=lambda y: y.weight)]


class CohortFeature(db.Model):
    __tablename__ = 'cohort_features'

    id = Column(Integer, primary_key=True)

    cohort_id = Column(Integer, ForeignKey('cohorts.id'))
    cohort = relationship('Cohort')

    name = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)

Index('cohort_features_cohort_id_idx', CohortFeature.cohort_id)


class CohortPatient(db.Model, MetaModelMixin):
    __tablename__ = 'cohort_patients'

    id = Column(Integer, primary_key=True)

    cohort_id = Column(Integer, ForeignKey('cohorts.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    cohort = relationship('Cohort')

    patient_id = Column(Integer, ForeignKey('patients.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    patient = relationship('Patient')

    recruited_by_organisation_id = Column(Integer, ForeignKey('organisations.id'), nullable=False)
    recruited_by_organisation = relationship('Organisation')

    is_active = Column(Boolean, nullable=False, default=True)

    __table_args__ = (
        UniqueConstraint('cohort_id', 'patient_id'),
    )

Index('cohort_patients_cohort_id_idx', CohortPatient.cohort_id)
Index('cohort_patients_patient_id_idx', CohortPatient.patient_id)


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

    @hybrid_method
    def has_permission(self, permission):
        # TODO
        raise NotImplementedError()

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

Index('cohort_users_cohort_id_idx', CohortUser.cohort_id)
Index('cohort_users_user_id_idx', CohortUser.user_id)


class CohortResultGroupSpec(db.Model):
    __tablename__ = 'cohort_result_group_specs'

    id = Column(Integer, primary_key=True)

    cohort_id = Column(Integer, ForeignKey('cohorts.id'), nullable=False)
    cohort = relationship('Cohort')

    result_group_spec_id = Column(Integer, ForeignKey('result_group_specs.id'), nullable=False)
    result_group_spec = relationship('ResultGroupSpec')

    weight = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('cohort_id', 'result_group_spec_id'),
    )

Index('cohort_result_group_specs_cohort_id_idx', CohortResultGroupSpec.cohort_id)

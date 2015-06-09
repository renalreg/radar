from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.lib.roles import DISEASE_GROUP_VIEW_DEMOGRAPHICS_ROLES, DISEASE_GROUP_VIEW_PATIENT_ROLES, \
    DISEASE_GROUP_VIEW_USER_ROLES, DISEASE_GROUP_MANAGED_ROLES, DISEASE_GROUP_ROLE_NAMES
from radar.models.common import MetadataMixin


class DiseaseGroup(db.Model):
    __tablename__ = 'disease_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    disease_group_patients = relationship('DiseaseGroupPatient')
    disease_group_users = relationship('DiseaseGroupUser')
    features = relationship('DiseaseGroupFeature')
    disease_group_result_group_definitions = relationship('DiseaseGroupResultGroupDefinition')

    @property
    def patients(self):
        return [x.patient for x in self.disease_group_patients]

    @property
    def users(self):
        return [x.user for x in self.disease_group_users]

    @property
    def result_group_definitions(self):
        return [x.result_group_definition for x in self.disease_group_result_group_definitions]

    def has_feature(self, name):
        return any(x.name == name for x in self.features)

    def can_view_patient(self, user):
        if user.is_admin:
            return True

        for disease_group_user in user.disease_groups:
            if disease_group_user.disease_group == self and disease_group_user.has_view_patient_permission:
                return True

        return False


class DiseaseGroupFeature(db.Model):
    __tablename__ = 'disease_group_features'

    id = Column(Integer, primary_key=True)

    disease_group_id = Column(Integer, ForeignKey('disease_groups.id'))
    disease_group = relationship('DiseaseGroup')

    name = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)


class DiseaseGroupPatient(db.Model, MetadataMixin):
    __tablename__ = 'disease_group_patients'

    id = Column(Integer, primary_key=True)

    disease_group_id = Column(Integer, ForeignKey('disease_groups.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    disease_group = relationship('DiseaseGroup')

    patient_id = Column(Integer, ForeignKey('patients.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    patient = relationship('Patient')

    is_active = Column(Boolean, nullable=False, default=True, server_default='1')

    __table_args__ = (
        UniqueConstraint('disease_group_id', 'patient_id'),
    )

    def can_edit(self, current_user):
        # TODO
        return self.patient.can_edit(current_user)


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


class DiseaseGroupResultGroupDefinition(db.Model):
    __tablename__ = 'disease_group_result_group_definitions'

    id = Column(Integer, primary_key=True)

    disease_group_id = Column(Integer, ForeignKey('disease_groups.id'), nullable=False)
    disease_group = relationship('DiseaseGroup')

    result_group_definition_id = Column(Integer, ForeignKey('result_group_definitions.id'), nullable=False)
    result_group_definition = relationship('ResultGroupDefinition')

    weight = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('disease_group_id', 'result_group_definition_id'),
    )

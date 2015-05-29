from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from radar.lib.database import db


class DiseaseGroup(db.Model):
    __tablename__ = 'disease_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    patients = relationship('DiseaseGroupPatient')
    users = relationship('DiseaseGroupUser')
    features = relationship('DiseaseGroupFeatures', backref='disease_group')

    def has_feature(self, feature_name):
        return any(x.feature_name == feature_name for x in self.features)

    def can_view_patient(self, user):
        if user.is_admin:
            return True

        for disease_group_user in user.disease_groups:
            if disease_group_user.disease_group == self and disease_group_user.has_view_patient_permission:
                return True

        return False


class DiseaseGroupFeatures(db.Model):
    __tablename__ = 'disease_group_features'

    id = Column(Integer, primary_key=True)
    disease_group_id = Column(Integer, ForeignKey('disease_groups.id'))
    feature_name = Column(String, nullable=False)
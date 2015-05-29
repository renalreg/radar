from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.models.common import MetadataMixin


class Diagnosis(db.Model, MetadataMixin):
    __tablename__ = 'diagnosis'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    disease_group_id = Column(Integer, ForeignKey('disease_groups.id'), nullable=False)
    disease_group = relationship('DiseaseGroup')

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)
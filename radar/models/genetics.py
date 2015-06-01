from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.models.common import MetadataMixin


class Genetics(db.Model, MetadataMixin):
    __tablename__ = 'genetics'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    disease_group_id = Column(Integer, ForeignKey('disease_groups.id'), nullable=False)
    disease_group = relationship('DiseaseGroup')

    sample_sent = Column(Boolean, nullable=False)
    sample_sent_date = Column(DateTime(timezone=True))
    laboratory = Column(String)
    laboratory_reference_number = Column(String)
    results = Column(Text)

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)
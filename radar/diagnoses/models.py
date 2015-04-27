from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from radar.models import DataSource


class Diagnosis(DataSource):
    __tablename__ = 'diagnoses'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship('Patient')

    disease_group_id = Column(Integer, ForeignKey('disease_groups.id'))
    disease_group = relationship('DiseaseGroup')

    diagnosis = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'diagnoses',
    }

    def to_concepts(self):
        return []
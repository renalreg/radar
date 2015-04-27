from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from radar.concepts import PatientConcept
from radar.database import Base
from radar.models import DataSource


class Demographics(DataSource):
    __tablename__ = 'demographics'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship('Patient')

    first_name = Column(String)
    last_name = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'demographics',
    }

    # TODO
    def to_concepts(self):
        return [
            (
                PatientConcept(self.first_name, self.last_name),
                [
                    ('first_name', 'first_name'),
                    ('last_name', 'last_name'),
                ]
            ),
        ]
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from radar.concepts import PatientConcept
from radar.database import Base


class Demographics(Base):
    __tablename__ = 'demographics'

    id = Column(Integer, ForeignKey('patients.id'), primary_key=True)
    patient = relationship('Patient')

    first_name = Column(String)
    last_name = Column(String)

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
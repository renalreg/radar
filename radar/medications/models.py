from sqlalchemy import Column, Date, String, ForeignKey

from sqlalchemy import Integer
from sqlalchemy.orm import relationship
from radar.concepts import MedicationConcept
from radar.database import Base


class Medication(Base):
    __tablename__ = 'medications'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship('Patient')

    from_date = Column(Date)
    to_date = Column(Date)
    name = Column(String)

    def to_concepts(self):
        return [
            (
                MedicationConcept(self.from_date, self.to_date, self.name),
                [
                    ('from_date', 'from_date'),
                    ('to_date', 'to_date'),
                    ('name', 'name'),
                ]
            ),
            (
                MedicationConcept(self.from_date, self.to_date, self.name),
                [
                    ('from_date', 'from_date'),
                    ('to_date', 'to_date'),
                    ('name', 'name'),
                ]
            )
        ]
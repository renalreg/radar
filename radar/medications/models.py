from sqlalchemy import Column, Date, String, ForeignKey

from sqlalchemy import Integer
from sqlalchemy.orm import relationship
from radar.concepts import MedicationConcept
from radar.models import DataSource


class Medication(DataSource):
    __tablename__ = 'medications'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship('Patient')

    from_date = Column(Date)
    to_date = Column(Date)
    name = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'medications',
    }

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)

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
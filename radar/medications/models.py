from flask import url_for
from sqlalchemy import Column, Date, String, ForeignKey

from sqlalchemy import Integer
from sqlalchemy.orm import relationship
from radar.medications.concepts import MedicationToMedicationConcept
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
            MedicationToMedicationConcept(self)
        ]

    def view_url(self):
        return url_for('medications.view_medication', patient_id=self.patient.id, medication_id=self.id)

    def edit_url(self):
        return url_for('medications.edit_medication', patient_id=self.patient.id, medication_id=self.id)

    def delete_url(self):
        return url_for('medications.delete_medication', patient_id=self.patient.id, medication_id=self.id)
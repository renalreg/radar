from collections import defaultdict

from sqlalchemy import Column, Date, String, ForeignKey, Numeric
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.models.common import MetadataMixin, StringLookupTable


class Medication(db.Model, MetadataMixin):
    __tablename__ = 'medications'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    facility = relationship('Facility')

    from_date = Column(Date, nullable=False)
    to_date = Column(Date)

    name = Column(String, nullable=False)

    dose_quantity = Column(Numeric, nullable=False)

    dose_unit_id = Column(String, ForeignKey('medication_dose_units.id'), nullable=False)
    dose_unit = relationship('MedicationDoseUnit')

    frequency_id = Column(String, ForeignKey('medication_frequencies.id'), nullable=False)
    frequency = relationship('MedicationFrequency')

    route_id = Column(String, ForeignKey('medication_routes.id'), nullable=False)
    route = relationship('MedicationRoute')

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)


class MedicationFrequency(StringLookupTable):
    __tablename__ = 'medication_frequencies'


class MedicationRoute(StringLookupTable):
    __tablename__ = 'medication_routes'


class MedicationDoseUnit(StringLookupTable):
    __tablename__ = 'medication_dose_units'
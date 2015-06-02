from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from radar.lib.database import db

from radar.models.common import MetadataMixin


class Hospitalisation(db.Model, MetadataMixin):
    __tablename__ = 'hospitalisations'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    facility = relationship('Facility')

    date_of_admission = Column(DateTime(timezone=True))
    date_of_discharge = Column(DateTime(timezone=True))
    reason_for_admission = Column(Text)
    comments = Column(Text)

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)

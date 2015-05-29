from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.models.common import MetadataMixin


class Pathology(db.Model, MetadataMixin):
    __tablename__ = 'pathology'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    facility = relationship('Facility')

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)
from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, Boolean, DateTime
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.models.common import MetadataMixin


class RenalImaging(db.Model, MetadataMixin):
    __tablename__ = 'renal_imaging'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    facility = relationship('Facility')

    date = Column(DateTime(timezone=True))

    imaging_type = Column(String)

    right_present = Column(Boolean)
    right_type = Column(String)
    right_length = Column(Numeric)
    right_cysts = Column(Numeric)
    right_calcification = Column(String)
    right_nephrocalcinosis = Column(Boolean)
    right_nephrolithiasis = Column(Boolean)
    right_other_malformation = Column(String)

    left_present = Column(Boolean)
    left_type = Column(String)
    left_length = Column(Numeric)
    left_cysts = Column(Numeric)
    left_calcification = Column(String)
    left_nephrocalcinosis = Column(Boolean)
    left_nephrolithiasis = Column(Boolean)
    left_other_malformation = Column(String)

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)
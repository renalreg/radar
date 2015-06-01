from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.models.common import MetadataMixin, IntegerLookupTable


class Dialysis(db.Model, MetadataMixin):
    __tablename__ = 'dialysis'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    facility = relationship('Facility')

    from_date = Column(Date, nullable=False)
    to_date = Column(Date)

    dialysis_type_id = Column(Integer, ForeignKey('dialysis_types.id'), nullable=False)
    dialysis_type = relationship('DialysisType')

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)


class DialysisType(IntegerLookupTable):
    __tablename__ = 'dialysis_types'
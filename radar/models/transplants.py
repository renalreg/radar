from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.models.common import MetadataMixin, IntegerLookupTable


class Transplant(db.Model, MetadataMixin):
    __tablename__ = 'transplants'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    facility = relationship('Facility')

    transplant_date = Column(Date)
    transplant_type_id = Column(Integer, ForeignKey('transplant_types.id'), nullable=False)
    transplant_type = relationship('TransplantType')
    reoccurred = Column(Boolean)
    date_reoccurred = Column(Date)
    date_failure = Column(Date)

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)


class TransplantType(IntegerLookupTable):
    __tablename__ = 'transplant_types'
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import Date
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.models.common import MetadataMixin, IntegerLookupTable


class Plasmapheresis(db.Model, MetadataMixin):
    __tablename__ = 'plasmapheresis'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    facility = relationship('Facility')

    from_date = Column(Date, nullable=False)
    to_date = Column(Date)
    no_of_exchanges = Column(Integer)
    response_id = Column(Integer, ForeignKey('plasmapheresis_responses.id'))
    response = relationship('PlasmapheresisResponse')

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user)


class PlasmapheresisResponse(IntegerLookupTable):
    __tablename__ = 'plasmapheresis_responses'

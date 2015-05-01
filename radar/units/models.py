from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from radar.database import db


class Unit(db.Model):
    __tablename__ = 'units'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    facility_id = Column(Integer, ForeignKey('facilities.id'))
    facility = relationship('Facility')

    patients = relationship('UnitPatient')
    users = relationship('UnitUser')
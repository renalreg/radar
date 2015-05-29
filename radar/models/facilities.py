from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from radar.lib.database import db


class Facility(db.Model):
    __tablename__ = 'facilities'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)


class PatientLatestImport(db.Model):
    __tablename__ = 'patient_latest_imports'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    facility = relationship('Facility')

    last_import_date = Column(DateTime(timezone=True), nullable=False)

    mpiid = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('patient_id', 'facility_id'),
    )
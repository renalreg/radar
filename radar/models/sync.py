from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, DateTime, Text
from sqlalchemy.orm import relationship

from radar.lib.database import db


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


class PatientImportLog(db.Model):
    __tablename__ = 'patient_import_logs'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    facility = relationship('Facility')

    data = Column(Text)


class PatientExportLog(db.Model):
    __tablename__ = 'patient_export_logs'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data = Column(Text)
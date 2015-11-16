from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, DateTime, Text
from sqlalchemy.orm import relationship

from radar.database import db


class PatientLatestImport(db.Model):
    __tablename__ = 'patient_latest_imports'

    id = Column(Integer, primary_key=True)

    patient_id = patient_id_column()
    patient = patient_relationship()

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    last_import_date = Column(DateTime(timezone=True), nullable=False)

    mpiid = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('patient_id', 'data_source_id'),
    )


class PatientImportLog(db.Model):
    __tablename__ = 'patient_import_logs'

    id = Column(Integer, primary_key=True)

    patient_id = patient_id_column()
    patient = patient_relationship()

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    data = Column(Text)


class PatientExportLog(db.Model):
    __tablename__ = 'patient_export_logs'

    id = Column(Integer, primary_key=True)

    patient_id = patient_id_column()
    patient = patient_relationship()

    data = Column(Text)

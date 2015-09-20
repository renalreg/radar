from sqlalchemy import Column, Integer, ForeignKey, String, Index
from sqlalchemy.orm import relationship
from radar.lib.database import db
from radar.lib.models import MetaModelMixin


class PatientNumber(db.Model, MetaModelMixin):
    __tablename__ = 'patient_numbers'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    organisation_id = Column(Integer, ForeignKey('organisations.id'), nullable=False)
    organisation = relationship('Organisation')

    number = Column(String, nullable=False)

Index('patient_numbers_patient_id_idx', PatientNumber.patient_id)
Index('patient_numbers_organisation_id_idx', PatientNumber.organisation_id)

from sqlalchemy import Column, Integer, ForeignKey, String, Index
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models import MetaModelMixin
from radar.models.common import UUIDPKColumn


class PatientNumber(db.Model, MetaModelMixin):
    __tablename__ = 'patient_numbers'

    id = UUIDPKColumn()

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    organisation_id = Column(Integer, ForeignKey('organisations.id'), nullable=False)
    organisation = relationship('Organisation')

    number = Column(String, nullable=False)

Index('patient_numbers_patient_id_idx', PatientNumber.patient_id)
Index('patient_numbers_organisation_id_idx', PatientNumber.organisation_id)

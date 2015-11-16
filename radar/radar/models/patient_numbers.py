from sqlalchemy import Column, Integer, ForeignKey, String, Index
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models import MetaModelMixin
from radar.models.common import uuid_pk_column, patient_id_column, patient_relationship


class PatientNumber(db.Model, MetaModelMixin):
    __tablename__ = 'patient_numbers'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('patient_numbers')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    organisation_id = Column(Integer, ForeignKey('organisations.id'), nullable=False)
    organisation = relationship('Organisation')

    number = Column(String, nullable=False)

Index('patient_numbers_patient_id_idx', PatientNumber.patient_id)
Index('patient_numbers_organisation_id_idx', PatientNumber.organisation_id)

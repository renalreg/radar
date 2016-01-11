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

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group', foreign_keys=[source_group_id])
    source_type_id = Column(String, ForeignKey('source_types.id'), nullable=False)
    source_type = relationship('SourceType')

    number_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    number_group = relationship('Group', foreign_keys=[number_group_id])
    number = Column(String, nullable=False)

Index(
    'patient_numbers_source_number_idx',
    PatientNumber.source_group_id,
    PatientNumber.number_group_id,
    PatientNumber.number,
    unique=True
)

Index('patient_numbers_patient_idx', PatientNumber.patient_id)
Index('patient_numbers_source_group_idx', PatientNumber.source_group_id)
Index('patient_numbers_number_group_idx', PatientNumber.number_group_id)

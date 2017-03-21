from sqlalchemy import Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship, uuid_pk_column
from radar.models.logs import log_changes


@log_changes
class PatientNumber(db.Model, MetaModelMixin):
    __tablename__ = 'patient_numbers'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('patient_numbers')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group', foreign_keys=[source_group_id])
    source_type = Column(String, nullable=False)

    number_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    number_group = relationship('Group', foreign_keys=[number_group_id])
    number = Column(String, nullable=False)


# Ensure patient numbers are unique across a source
Index(
    'patient_numbers_source_number_idx',
    PatientNumber.source_group_id,
    PatientNumber.source_type,
    PatientNumber.number_group_id,
    PatientNumber.number,
    unique=True
)

# Ensure patient's don't have more than one number for each type
# TODO disabled until existing data is cleaned up
# Index(
#    'patient_numbers_patient_number_idx',
#    PatientNumber.patient_id,
#    PatientNumber.source_group_id,
#    PatientNumber.source_type,
#    PatientNumber.number_group_id,
#    unique=True
# )

Index('patient_numbers_patient_idx', PatientNumber.patient_id)
Index('patient_numbers_source_group_idx', PatientNumber.source_group_id)
Index('patient_numbers_number_group_idx', PatientNumber.number_group_id)

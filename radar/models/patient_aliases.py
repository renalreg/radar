from sqlalchemy import Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship, uuid_pk_column
from radar.models.logs import log_changes


@log_changes
class PatientAlias(db.Model, MetaModelMixin):
    __tablename__ = 'patient_aliases'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('patient_aliases')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_type = Column(String, nullable=False)

    first_name = Column(String)
    last_name = Column(String)

Index('patient_aliases_patient_idx', PatientAlias.patient_id)

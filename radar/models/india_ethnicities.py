from sqlalchemy import Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship, uuid_pk_column
from radar.models.logs import log_changes


@log_changes
class IndiaEthnicity(db.Model, MetaModelMixin):
    __tablename__ = 'india_ethnicities'

    id = uuid_pk_column()
    patient_id = patient_id_column()
    patient = patient_relationship('india_ethnicities')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group', foreign_keys=[source_group_id])
    source_type = Column(String, nullable=False)

    father_ancestral_state = Column(String)
    father_language = Column(String)
    mother_ancestral_state = Column(String)
    mother_language = Column(String)


Index('india_ethnicity_patient_idx', IndiaEthnicity.patient_id)

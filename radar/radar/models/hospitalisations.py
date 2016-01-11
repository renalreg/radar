from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, Index, String
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship


class Hospitalisation(db.Model, MetaModelMixin):
    __tablename__ = 'hospitalisations'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('hospitalisations')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_type_id = Column(String, ForeignKey('source_types.id'), nullable=False)
    source_type = relationship('SourceType')

    date_of_admission = Column(DateTime(timezone=True), nullable=False)
    date_of_discharge = Column(DateTime(timezone=True))
    reason_for_admission = Column(Text)
    comments = Column(Text)

Index('hospitalisations_patient_idx', Hospitalisation.patient_id)

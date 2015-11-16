from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, Index
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship


class Hospitalisation(db.Model, MetaModelMixin):
    __tablename__ = 'hospitalisations'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('hospitalisations')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    date_of_admission = Column(DateTime(timezone=True), nullable=False)
    date_of_discharge = Column(DateTime(timezone=True))
    reason_for_admission = Column(Text)
    comments = Column(Text)

Index('hospitalisations_patient_id_idx', Hospitalisation.patient_id)

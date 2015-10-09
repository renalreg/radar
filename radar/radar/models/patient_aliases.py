from sqlalchemy import String, Column, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from radar.database import db
from radar.models import MetaModelMixin


class PatientAlias(db.Model, MetaModelMixin):
    __tablename__ = 'patient_aliases'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    first_name = Column(String)
    last_name = Column(String)

Index('patient_aliases_patient_id_idx', PatientAlias.patient_id)

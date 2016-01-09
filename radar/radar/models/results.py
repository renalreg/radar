from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship

OBSERVATION_TYPE_INTEGER = 'INTEGER'
OBSERVATION_TYPE_REAL = 'REAL'
OBSERVATION_TYPE_LOOKUP = 'LOOKUP'
OBSERVATION_TYPE_STRING = 'STRING'


class Observation(db.Model):
    __tablename__ = 'observations'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)


class Result(db.Model, MetaModelMixin):
    __tablename__ = 'results'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('results')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    observation_id = Column(Integer, ForeignKey('observations.id'), nullable=False)
    observation = relationship('Observation')

    date = Column(DateTime(timezone=False), nullable=False)
    value = Column(String, nullable=False)

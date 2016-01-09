from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

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
    short_name = Column(String, nullable=False)
    system_id = Column(Integer, ForeignKey('observation_systems.id'), nullable=False)
    system = relationship('ObservationSystem')
    options = Column(JSONB, nullable=False)


class ObservationSystem(db.Model):
    __tablename__ = 'observation_systems'

    id = Column(Integer, primary_key=True)
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
    _value = Column('value', String, nullable=False)

    @property
    def value(self):
        x = self._value

        if self.observation:
            observation_type = self.observation

            if observation_type == OBSERVATION_TYPE_INTEGER:
                x = int(x)
            elif observation_type == OBSERVATION_TYPE_REAL:
                x = float(x)

        return x

    @value.setter
    def value(self, x):
        if x is not None:
            x = str(x)

        self._value = x

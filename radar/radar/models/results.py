from collections import OrderedDict

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from enum import Enum

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship
from radar.models.types import EnumType


class OBSERVATION_VALUE_TYPE(Enum):
    INTEGER = 'INTEGER'
    REAL = 'REAL'
    ENUM = 'ENUM'
    STRING = 'STRING'


OBSERVATION_VALUE_TYPE_NAMES = OrderedDict([
    (OBSERVATION_VALUE_TYPE.INTEGER, 'Integer'),
    (OBSERVATION_VALUE_TYPE.REAL, 'Real'),
    (OBSERVATION_VALUE_TYPE.ENUM, 'Enum'),
    (OBSERVATION_VALUE_TYPE.STRING, 'String'),
])


class OBSERVATION_SAMPLE_TYPE(Enum):
    URINE = 'URINE'
    BLOOD = 'BLOOD'
    URINE_DIPSTICK = 'URINE_DIPSTICK'
    OBSERVATION = 'OBSERVATION'


OBSERVATION_SAMPLE_TYPE_NAMES = OrderedDict([
    (OBSERVATION_SAMPLE_TYPE.BLOOD, 'Blood'),
    (OBSERVATION_SAMPLE_TYPE.URINE, 'Urine'),
    (OBSERVATION_SAMPLE_TYPE.URINE_DIPSTICK, 'Urine Dipstick'),
    (OBSERVATION_SAMPLE_TYPE.OBSERVATION, 'Observation'),
])


class Observation(db.Model):
    __tablename__ = 'observations'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    value_type = Column(EnumType(OBSERVATION_VALUE_TYPE, name='observation_value_type'), nullable=False)
    sample_type = Column(EnumType(OBSERVATION_SAMPLE_TYPE, name='observation_sample_type'), nullable=False)
    pv_code = Column(String)
    properties = Column(postgresql.JSONB, nullable=False)


class Result(db.Model, MetaModelMixin):
    __tablename__ = 'results'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('results')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_type = Column(String, nullable=False)

    observation_id = Column(Integer, ForeignKey('observations.id'), nullable=False)
    observation = relationship('Observation')

    date = Column(DateTime(timezone=True), nullable=False)
    _value = Column('value', String, nullable=False)

    @property
    def value(self):
        x = self._value

        if x is not None and self.observation is not None:
            value_type = self.observation.value_type

            if value_type == OBSERVATION_VALUE_TYPE.INTEGER:
                x = int(x)
            elif value_type == OBSERVATION_VALUE_TYPE.REAL:
                x = float(x)

        return x

    @value.setter
    def value(self, x):
        if x is not None:
            x = str(x)

        self._value = x

Index('results_patient_idx', Result.patient_id)

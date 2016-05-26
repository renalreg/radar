from collections import OrderedDict

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from enum import Enum

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship
from radar.models.types import EnumType
from radar.models.logs import log_changes


class OBSERVATION_VALUE_TYPE(Enum):
    INTEGER = 'INTEGER'
    REAL = 'REAL'
    ENUM = 'ENUM'
    STRING = 'STRING'

    def __str__(self):
        return str(self.value)


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

    def __str__(self):
        return str(self.value)


OBSERVATION_SAMPLE_TYPE_NAMES = OrderedDict([
    (OBSERVATION_SAMPLE_TYPE.BLOOD, 'Blood'),
    (OBSERVATION_SAMPLE_TYPE.URINE, 'Urine'),
    (OBSERVATION_SAMPLE_TYPE.URINE_DIPSTICK, 'Urine Dipstick'),
    (OBSERVATION_SAMPLE_TYPE.OBSERVATION, 'Observation'),
])


@log_changes
class Observation(db.Model):
    __tablename__ = 'observations'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    value_type = Column(EnumType(OBSERVATION_VALUE_TYPE, name='observation_value_type'), nullable=False)
    sample_type = Column(EnumType(OBSERVATION_SAMPLE_TYPE, name='observation_sample_type'), nullable=False)
    pv_code = Column(String)
    properties = Column(postgresql.JSONB, nullable=False)

    @property
    def min_value(self):
        return self.properties.get('min_value')

    @property
    def max_value(self):
        return self.properties.get('max_value')

    @property
    def min_length(self):
        return self.properties.get('min_length')

    @property
    def max_length(self):
        return self.properties.get('max_length')

    @property
    def units(self):
        return self.properties.get('units')

    @property
    def options(self):
        return self.properties.get('options', [])

    @property
    def options_map(self):
        return dict((x['code'], x['description']) for x in self.options)


@log_changes
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

    @property
    def value_description(self):
        if self.observation.value_type == OBSERVATION_VALUE_TYPE.ENUM:
            return self.observation.options_map.get(self.value)
        else:
            return None

Index('results_patient_idx', Result.patient_id)

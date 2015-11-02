from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, UniqueConstraint, DateTime, Index, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models import MetaModelMixin
from radar.models.common import uuid_pk_column

RESULT_SPEC_TYPE_INTEGER = 'INTEGER'
RESULT_SPEC_TYPE_FLOAT = 'FLOAT'
RESULT_SPEC_TYPE_STRING = 'STRING'
RESULT_SPEC_TYPE_CODED_STRING = 'CODED_STRING'
RESULT_SPEC_TYPE_CODED_INTEGER = 'CODED_INTEGER'

RESULT_SPEC_TYPES = [
    RESULT_SPEC_TYPE_INTEGER,
    RESULT_SPEC_TYPE_FLOAT,
    RESULT_SPEC_TYPE_STRING,
    RESULT_SPEC_TYPE_CODED_STRING,
    RESULT_SPEC_TYPE_CODED_INTEGER
]


class ResultGroup(db.Model, MetaModelMixin):
    __tablename__ = 'result_groups'

    id = uuid_pk_column()

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    result_group_spec_id = Column(Integer, ForeignKey('result_group_specs.id'), nullable=False)
    result_group_spec = relationship('ResultGroupSpec')

    date = Column(DateTime(timezone=True), nullable=False)
    results = Column(JSONB, nullable=False)

Index('result_groups_patient_id_idx', ResultGroup.patient_id)
Index('result_groups_results_gin', ResultGroup.results, postgresql_using='gin')


class ResultGroupSpec(db.Model):
    __tablename__ = 'result_group_specs'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)

    result_group_result_specs = relationship('ResultGroupResultSpec')

    @property
    def result_specs(self):
        return [x.result_spec for x in self.result_group_result_specs]

    @property
    def sorted_result_specs(self):
        return [x.result_spec for x in sorted(self.result_group_result_specs, key=lambda y: y.weight)]


class ResultSpec(db.Model):
    __tablename__ = 'result_specs'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    type = Column(String, nullable=False)

    # For INTEGER and DECIMAL types
    min_value = Column(Numeric, nullable=True)
    max_value = Column(Numeric, nullable=True)
    units = Column(String, nullable=True)

    # For STRING type
    min_length = Column(Integer, nullable=True)
    max_length = Column(Integer, nullable=True)

    # For SELECT type
    options = Column(JSONB, nullable=True)

    # Controls whether this value will be grouped with values from other result groups
    # True if this value gives context to the other data in this result group (e.g. pre/post dialysis)
    meta = Column(Boolean, nullable=False)

    @property
    def options_as_dict(self):
        return {x['id']: x['label'] for x in self.options}

    @property
    def option_values(self):
        return [x['id'] for x in self.options]


class ResultGroupResultSpec(db.Model):
    __tablename__ = 'result_group_result_specs'

    id = Column(Integer, primary_key=True)

    result_group_spec_id = Column(Integer, ForeignKey('result_group_specs.id'), nullable=False)
    result_group_spec = relationship('ResultGroupSpec')

    result_spec_id = Column(Integer, ForeignKey('result_specs.id'), nullable=False)
    result_spec = relationship('ResultSpec')

    weight = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('result_group_spec_id', 'result_spec_id'),
    )

Index('result_group_result_specs_result_group_spec_id_idx', ResultGroupResultSpec.result_group_spec_id)
Index('result_group_result_specs_result_spec_id_idx', ResultGroupResultSpec.result_spec_id)

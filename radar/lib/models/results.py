from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Boolean, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.lib.models import MetaModelMixin

RESULT_SPEC_TYPE_INTEGER = 'INTEGER'
RESULT_SPEC_TYPE_DECIMAL = 'DECIMAL'
RESULT_SPEC_TYPE_STRING = 'STRING'
RESULT_SPEC_TYPE_SELECT = 'SELECT'

RESULT_SPEC_TYPES = [
    RESULT_SPEC_TYPE_INTEGER,
    RESULT_SPEC_TYPE_DECIMAL,
    RESULT_SPEC_TYPE_STRING,
    RESULT_SPEC_TYPE_SELECT
]


class ResultGroup(db.Model, MetaModelMixin):
    __tablename__ = 'result_groups'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    result_group_spec_id = Column(Integer, ForeignKey('result_group_specs.id'), nullable=False)
    result_group_spec = relationship('ResultGroupSpec')

    date = Column(DateTime(timezone=True), nullable=False)

    results = relationship('Result')


class Result(db.Model):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)

    result_group_id = Column(Integer, ForeignKey('result_groups.id'), nullable=False)
    result_group = relationship('ResultGroup')

    result_spec_id = Column(Integer, ForeignKey('result_specs.id'), nullable=False)
    result_spec = relationship('ResultSpec')

    value = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('result_group_id', 'result_spec_id'),
    )


class ResultGroupSpec(db.Model):
    __tablename__ = 'result_group_specs'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)

    result_group_result_specs = relationship('ResultGroupResultSpec')

    @property
    def sorted_results(self):
        return [x.result_spec for x in sorted(self.result_group_result_specs, key=lambda y: y.weight)]


class ResultSpec(db.Model):
    __tablename__ = 'result_specs'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    type = Column(String, nullable=False)

    # For INTEGER and DECIMAL types
    min_value = Column(Numeric)
    max_value = Column(Numeric)
    units = Column(String)

    # For SELECT type
    result_select_id = Column(Integer, ForeignKey('result_selects.id'), nullable=True)
    result_select = relationship('ResultSelect')


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


class ResultSelect(db.Model):
    __tablename__ = 'result_selects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    result_options = relationship('ResultOption')

    @property
    def sorted_options(self):
        return sorted(self.result_options, key=lambda x: x.weight)


class ResultOption(db.Model):
    __tablename__ = 'result_options'

    id = Column(Integer, primary_key=True)

    result_select_id = Column(String, ForeignKey('result_selects.id'), nullable=False)
    result_select = relationship('ResultSelect')

    value = Column(String, nullable=False)
    label = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)

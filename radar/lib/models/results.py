from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Boolean, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.lib.models import MetaModelMixin


class ResultGroup(db.Model, MetaModelMixin):
    __tablename__ = 'result_groups'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    result_group_definition_id = Column(Integer, ForeignKey('result_group_definitions.id'), nullable=False)
    result_group_definition = relationship('ResultGroupDefinition')

    date = Column(DateTime(timezone=True), nullable=False)
    pre_post = Column(String)

    results = relationship('Result', cascade='all, delete-orphan')

    @property
    def sorted_results(self):
        """ Return lab results in the correct order (by weight) """

        results_dict = {}

        for result in self.results:
            results_dict[result.result_definition.id] = result

        output = []

        for result_definition in self.result_group_definition.result_definitions:
            result = results_dict.get(result_definition.id)

            if result is not None:
                output.append(result)

        return output


class Result(db.Model):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)

    result_group_id = Column(Integer, ForeignKey('result_groups.id'), nullable=False)
    result_group = relationship('ResultGroup')

    result_definition_id = Column(Integer, ForeignKey('result_definitions.id'), nullable=False)
    result_definition = relationship('ResultDefinition')

    value = Column(Numeric, nullable=False)

    __table_args__ = (
        UniqueConstraint('result_group_id', 'result_definition_id'),
    )


class ResultGroupDefinition(db.Model):
    __tablename__ = 'result_group_definitions'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    pre_post = Column(Boolean, nullable=False)

    result_group_result_definitions = relationship('ResultGroupResultDefinition')

    @property
    def result_definitions(self):
        return [x.result_definition for x in sorted(self.result_group_result_definitions, key=lambda y: y.weight)]


class ResultDefinition(db.Model):
    __tablename__ = 'result_definitions'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    units = Column(String)
    min_value = Column(Numeric)
    max_value = Column(Numeric)

    result_group_result_definitions = relationship('ResultGroupResultDefinition')


class ResultGroupResultDefinition(db.Model):
    __tablename__ = 'result_group_result_definitions'

    id = Column(Integer, primary_key=True)

    result_group_definition_id = Column(Integer, ForeignKey('result_group_definitions.id'), nullable=False)
    result_group_definition = relationship('ResultGroupDefinition')

    result_definition_id = Column(Integer, ForeignKey('result_definitions.id'), nullable=False)
    result_definition = relationship('ResultDefinition')

    weight = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('result_group_definition_id', 'result_definition_id'),
    )

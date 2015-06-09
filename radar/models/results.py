from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Boolean, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.models import MetadataMixin


class ResultGroup(db.Model, MetadataMixin):
    __tablename__ = 'result_groups'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    facility = relationship('Facility')

    result_group_definition_id = Column(Integer, ForeignKey('result_group_definitions.id'), nullable=False)
    result_group_definition = relationship('ResultGroupDefinition')

    date = Column(DateTime(timezone=True), nullable=False)
    pre_post = Column(String)  # TODO constraint

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

    def can_view(self, current_user):
        return self.patient.can_view(current_user)

    def can_edit(self, current_user):
        return self.patient.can_edit(current_user)


class Result(db.Model):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)

    result_group_id = Column(Integer, ForeignKey('result_groups.id'), nullable=False)
    result_group = relationship('ResultGroup')

    result_definition_id = Column(Integer, ForeignKey('result_definitions.id'), nullable=False)
    result_definition = relationship('ResultDefinition')

    value = Column(Numeric, nullable=False)

    # TODO re-enable - need to figure out how to delete children before adding new ones (see populate_obj)
    #__table_args__ = (
    #   UniqueConstraint('result_group_id', 'result_definition_id'),
    #)

    def can_view(self, current_user):
        return self.result_group.patient.can_view(current_user)

    def can_edit(self, current_user):
        return self.result_group.patient.can_edit(current_user)


class ResultGroupDefinition(db.Model):
    __tablename__ = 'result_group_definitions'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)  # TODO force casing
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    pre_post = Column(Boolean, nullable=False)

    result_group_result_definitions = relationship('ResultGroupResultDefinition')

    @classmethod
    def find_by_code(cls, code):
        return cls.query.filter(cls.code == code).first()

    @property
    def result_definitions(self):
        return [x.result_definition for x in sorted(self.result_group_result_definitions, key=lambda y: y.weight)]


class ResultDefinition(db.Model):
    __tablename__ = 'result_definitions'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)  # TODO force casing
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    units = Column(String)
    min_value = Column(Numeric)
    max_value = Column(Numeric)

    result_group_result_definitions = relationship('ResultGroupResultDefinition')

    @classmethod
    def find_by_code(cls, code):
        return cls.query.filter(cls.code == code).first()


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

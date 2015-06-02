from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date, Boolean, UniqueConstraint, DateTime

from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.models import MetadataMixin


class LabGroup(db.Model, MetadataMixin):
    __tablename__ = 'lab_groups'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    facility = relationship('Facility')

    lab_group_definition_id = Column(Integer, ForeignKey('lab_group_definitions.id'), nullable=False)
    lab_group_definition = relationship('LabGroupDefinition')

    date = Column(DateTime(timezone=True), nullable=False)
    pre_post = Column(String)

    lab_results = relationship('LabResult')

    def can_view(self, current_user):
        return self.patient.can_view(current_user)

    def can_edit(self, current_user):
        return self.patient.can_edit(current_user)


class LabResult(db.Model):
    __tablename__ = 'lab_results'

    id = Column(Integer, primary_key=True)

    lab_group_id = Column(Integer, ForeignKey('lab_groups.id'), nullable=False)
    lab_group = relationship('LabGroup')

    lab_result_definition_id = Column(Integer, ForeignKey('lab_result_definitions.id'), nullable=False)
    lab_result_definition = relationship('LabResultDefinition')

    value = Column(Numeric, nullable=False)

    __table_args__ = (
        UniqueConstraint('lab_group_id', 'lab_result_definition_id'),
    )

    def can_view(self, current_user):
        return self.lab_group.patient.can_view(current_user)

    def can_edit(self, current_user):
        return self.lab_group.patient.can_edit(current_user)


class LabGroupDefinition(db.Model):
    __tablename__ = 'lab_group_definitions'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    pre_post = Column(Boolean, nullable=False)

    lab_group_result_definitions = relationship('LabGroupResultDefinition')

    @classmethod
    def find_by_code(cls, code):
        return cls.query.filter(cls.code == code).first()


class LabResultDefinition(db.Model):
    __tablename__ = 'lab_result_definitions'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    units = Column(String)
    min_value = Column(Numeric)
    max_value = Column(Numeric)

    lab_group_result_definitions = relationship('LabGroupResultDefinition')

    @classmethod
    def find_by_code(cls, code):
        return cls.query.filter(cls.code == code).first()


class LabGroupResultDefinition(db.Model):
    __tablename__ = 'lab_group_result_definitions'

    id = Column(Integer, primary_key=True)

    lab_group_definition_id = Column(Integer, ForeignKey('lab_group_definitions.id'), nullable=False)
    lab_group_definition = relationship('LabGroupDefinition')

    lab_result_definition_id = Column(Integer, ForeignKey('lab_result_definitions.id'), nullable=False)
    lab_result_definition = relationship('LabResultDefinition')

    weight = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('lab_group_definition_id', 'lab_result_definition_id'),
    )
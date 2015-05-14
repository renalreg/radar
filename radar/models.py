from datetime import datetime
from flask_login import current_user

from sqlalchemy import Integer, Column, String, ForeignKey, UniqueConstraint, DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy import event

from radar.database import db


class UnitPatient(db.Model):
    __tablename__ = 'unit_patients'

    id = Column(Integer, primary_key=True)

    unit_id = Column(Integer, ForeignKey('units.id'), nullable=False)
    unit = relationship('Unit')

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    created_date = Column(DateTime(timezone=True), default=datetime.now)
    created_user_id = Column(Integer, ForeignKey('users.id'))
    created_user = relationship('User')

    __table_args__ = (
        UniqueConstraint('unit_id', 'patient_id'),
    )


class DiseaseGroupPatient(db.Model):
    __tablename__ = 'disease_group_patients'

    id = Column(Integer, primary_key=True)

    disease_group_id = Column(Integer, ForeignKey('disease_groups.id'), nullable=False)
    disease_group = relationship('DiseaseGroup')

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    created_date = Column(DateTime(timezone=True), default=datetime.now)
    created_user_id = Column(Integer, ForeignKey('users.id'))
    created_user = relationship('User')

    __table_args__ = (
        UniqueConstraint('disease_group_id', 'patient_id'),
    )


class Facility(db.Model):
    __tablename__ = 'facilities'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)


class DataSource(db.Model):
    __tablename__ = 'data_sources'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    sda_bundle = relationship('SDABundle', uselist=False, cascade='all, delete-orphan')

    def view_url(self):
        return None

    def edit_url(self):
        return None

    def delete_url(self):
        return None

    def can_view(self, user):
        _ = user
        return False

    def can_edit(self, user):
        _ = user
        return False

    __mapper_args__ = {
        'polymorphic_identity': 'data_sources',
        'polymorphic_on': type
    }


class DataImport(DataSource):
    __tablename__ = 'data_imports'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'))
    facility_id = Column(Integer, ForeignKey('facilities.id'))

    patient = relationship('Patient')
    facility = relationship('Facility')

    __mapper_args__ = {
        'polymorphic_identity': 'data_imports',
    }

    __table_args__ = (
        UniqueConstraint('patient_id', 'facility_id'),
    )


class CreatedModifiedMixin(object):
    @declared_attr
    def created_user_id(cls):
        return Column(Integer, ForeignKey('users.id'))

    @declared_attr
    def created_user(cls):
        return relationship('User', foreign_keys=[cls.created_user_id])

    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now())

    @declared_attr
    def modified_user_id(cls):
        return Column(Integer, ForeignKey('users.id'))

    @declared_attr
    def modified_user(cls):
        return relationship('User', foreign_keys=[cls.modified_user_id])

    @declared_attr
    def modified_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())


class PatientMixin(object):
    @declared_attr
    def patient_id(cls):
        return Column(Integer, ForeignKey('patients.id'))

    @declared_attr
    def patient(cls):
        return relationship('Patient')


class DiseaseGroupMixin(object):
    @declared_attr
    def disease_group_id(cls):
        return Column(Integer, ForeignKey('disease_groups.id'))

    @declared_attr
    def disease_group(cls):
        return relationship('DiseaseGroup')


class UnitMixin(object):
    @declared_attr
    def unit_id(cls):
        return Column(Integer, ForeignKey('units.id'))

    @declared_attr
    def unit(cls):
        return relationship('Unit')


class LookupTableMixin(object):
    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True)

    @declared_attr
    def name(cls):
        return Column(String)

    @classmethod
    def choices(cls, session):
        return [(x.id, x.name, x) for x in session.query(cls).order_by(cls.name).all()]


class StringLookupTableMixin(object):
    @declared_attr
    def id(cls):
        return Column(String, primary_key=True)

    @declared_attr
    def name(cls):
        return Column(String)

    @classmethod
    def choices(cls, session):
        return [(x.id, x.name, x) for x in session.query(cls).order_by(cls.name).all()]
from sqlalchemy import Integer, Column, String, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship

from radar.database import db


class UnitPatient(db.Model):
    __tablename__ = 'unit_patients'

    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, ForeignKey('units.id'), nullable=False)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)

    unit = relationship('Unit')
    patient = relationship('Patient')

    __table_args__ = (
        UniqueConstraint('unit_id', 'patient_id'),
    )


class DiseaseGroupPatient(db.Model):
    __tablename__ = 'disease_group_patients'

    id = Column(Integer, primary_key=True)
    disease_group_id = Column(Integer, ForeignKey('disease_groups.id'), nullable=False)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)

    disease_group = relationship('DiseaseGroup')
    patient = relationship('Patient')

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
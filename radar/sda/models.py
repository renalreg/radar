from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from radar.database import db
from radar.utils import get_path, get_path_as_datetime

class SDAResource(db.Model):
    __tablename__ = 'sda_resources'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)
    data_source = relationship('DataSource')

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    facility = relationship('Facility')

    mpiid = Column(Integer)

    sda_medications = relationship('SDAMedication', cascade='all')
    sda_patient = relationship('SDAPatient', uselist=False, cascade='all')


class SDAMedication(db.Model):
    __tablename__ = 'sda_medications'

    id = Column(Integer, primary_key=True)
    sda_resource_id = Column(Integer, ForeignKey('sda_resources.id'))
    sda_resource = relationship('SDAResource')

    data = Column(JSONB)


class SDAPatient(db.Model):
    __tablename__ = 'sda_patients'

    id = Column(Integer, primary_key=True)

    sda_resource_id = Column(Integer, ForeignKey('sda_resources.id'))
    sda_resource = relationship('SDAResource')

    data = Column(JSONB)

    aliases = relationship('SDAPatientAlias', cascade='all')
    numbers = relationship('SDAPatientNumber', cascade='all')
    addresses = relationship('SDAPatientAddress', cascade='all')

    @hybrid_property
    def first_name(self):
        return get_path(self.data, 'name', 'given_name')

    @hybrid_property
    def last_name(self):
        return get_path(self.data, 'name', 'family_name')

    @hybrid_property
    def date_of_birth(self):
        return get_path_as_datetime(self.data, 'birth_time')

    @hybrid_property
    def gender(self):
        return get_path(self.data, 'gender', 'code')

    @first_name.expression
    def first_name(cls):
        return SDAPatient.data[('name', 'given_name')].astext

    @last_name.expression
    def last_name(cls):
        return SDAPatient.data[('name', 'family_name')].astext

    @date_of_birth.expression
    def date_of_birth(cls):
        return SDAPatient.data[('name', 'date_of_birth')].astext

    @gender.expression
    def gender(cls):
        return SDAPatient.data[('name', 'gender')].astext

class SDAPatientAlias(db.Model):
    __tablename__ = 'sda_patient_aliases'

    id = Column(Integer, primary_key=True)

    sda_patient_id = Column(Integer, ForeignKey('sda_patients.id'))
    sda_patient = relationship('SDAPatient')

    data = Column(JSONB)


class SDAPatientNumber(db.Model):
    __tablename__ = 'sda_patient_numbers'

    id = Column(Integer, primary_key=True)

    sda_patient_id = Column(Integer, ForeignKey('sda_patients.id'))
    sda_patient = relationship('SDAPatient')

    data = Column(JSONB)


class SDAPatientAddress(db.Model):
    __tablename__ = 'sda_patient_addresses'

    id = Column(Integer, primary_key=True)

    sda_patient_id = Column(Integer, ForeignKey('sda_patients.id'))
    sda_patient = relationship('SDAPatient')

    data = Column(JSONB)
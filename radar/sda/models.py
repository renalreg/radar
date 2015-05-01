from sqlalchemy import Integer, Column, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from radar.database import db
from radar.sda.utils import serialize_jsonb
from radar.utils import get_path_as_text, get_path_as_datetime


class SDABundle(db.Model):
    __tablename__ = 'sda_bundles'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)
    data_source = relationship('DataSource')

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    facility = relationship('Facility')

    mpiid = Column(Integer)

    sda_medications = relationship('SDAMedication', cascade='all')
    sda_patient = relationship('SDAPatient', uselist=False, cascade='all')

    def serialize(self):
        if self.sda_patient is not None:
            self.sda_patient.serialize()

        for x in self.sda_medications:
            x.serialize()


class SDAMedication(db.Model):
    __tablename__ = 'sda_medications'

    id = Column(Integer, primary_key=True)
    sda_bundle_id = Column(Integer, ForeignKey('sda_bundles.id'))
    sda_bundle = relationship('SDABundle')

    data = Column(JSONB)

    def serialize(self):
        self.data = serialize_jsonb(self.data)


class SDAPatient(db.Model):
    __tablename__ = 'sda_patients'

    id = Column(Integer, primary_key=True)

    sda_bundle_id = Column(Integer, ForeignKey('sda_bundles.id'))
    sda_bundle = relationship('SDABundle')

    data = Column(JSONB, nullable=False)

    aliases = relationship('SDAPatientAlias', cascade='all')
    numbers = relationship('SDAPatientNumber', cascade='all')
    addresses = relationship('SDAPatientAddress', cascade='all')

    @hybrid_property
    def first_name(self):
        return get_path_as_text(self.data, ['name', 'given_name'])

    @hybrid_property
    def last_name(self):
        return get_path_as_text(self.data, ['name', 'family_name'])

    @hybrid_property
    def date_of_birth(self):
        return get_path_as_datetime(self.data, ['birth_time'])

    @hybrid_property
    def gender(self):
        return get_path_as_text(self.data, ['gender', 'code'])

    @first_name.expression
    def first_name(cls):
        return SDAPatient.data[('name', 'given_name')].astext

    @last_name.expression
    def last_name(cls):
        return SDAPatient.data[('name', 'family_name')].astext

    @date_of_birth.expression
    def date_of_birth(cls):
        return func.parse_date_to_lower(SDAPatient.data['birth_time'].astext)

    @gender.expression
    def gender(cls):
        return SDAPatient.data[('name', 'gender')].astext

    def serialize(self):
        self.data = serialize_jsonb(self.data)

        for x in self.aliases:
            x.serialize()

        for x in self.numbers:
            x.serialize()

        for x in self.addresses:
            x.serialize()


class SDAPatientAlias(db.Model):
    __tablename__ = 'sda_patient_aliases'

    id = Column(Integer, primary_key=True)

    sda_patient_id = Column(Integer, ForeignKey('sda_patients.id'))
    sda_patient = relationship('SDAPatient')

    data = Column(JSONB, nullable=False)

    @hybrid_property
    def first_name(self):
        return get_path_as_text(self.data, ['given_name'])

    @hybrid_property
    def last_name(self):
       return get_path_as_text(self.data, ['family_name'])

    @first_name.expression
    def first_name(cls):
        return SDAPatient.data['given_name'].astext

    @last_name.expression
    def last_name(cls):
        return SDAPatient.data['family_name'].astext

    def serialize(self):
        self.data = serialize_jsonb(self.data)


class SDAPatientNumber(db.Model):
    __tablename__ = 'sda_patient_numbers'

    id = Column(Integer, primary_key=True)

    sda_patient_id = Column(Integer, ForeignKey('sda_patients.id'))
    sda_patient = relationship('SDAPatient')

    data = Column(JSONB, nullable=False)

    def serialize(self):
        self.data = serialize_jsonb(self.data)


class SDAPatientAddress(db.Model):
    __tablename__ = 'sda_patient_addresses'

    id = Column(Integer, primary_key=True)

    sda_patient_id = Column(Integer, ForeignKey('sda_patients.id'))
    sda_patient = relationship('SDAPatient')

    data = Column(JSONB, nullable=False)

    @property
    def from_time(self):
        return get_path_as_datetime(self.data, ['from_time'])

    @property
    def to_time(self):
        return get_path_as_datetime(self.data, ['to_time'])

    @property
    def full_address(self):
        parts = []

        street = get_path_as_text(self.data, ['street'])

        if street:
            parts.extend(street.split(";"))

        parts.extend([
            get_path_as_text(self.data, ['city', 'description']),
            get_path_as_text(self.data, ['state', 'description']),
            get_path_as_text(self.data, ['zip', 'description']),
            get_path_as_text(self.data, ['country', 'description']),
        ])

        return "\n".join(x for x in parts if x)

    def serialize(self):
        self.data = serialize_jsonb(self.data)
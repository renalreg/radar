from datetime import datetime

from sqlalchemy import Integer, Column, String, ForeignKey, UniqueConstraint, select, join, Boolean, \
    PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, aliased
from werkzeug.security import generate_password_hash, check_password_hash

from radar.database import Base
from radar.utils import get_path


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)

    units = relationship('UnitPatient')
    disease_groups = relationship('DiseaseGroupPatient')

    sda_resources = relationship('SDAResource')

    @hybrid_property
    def first_name(self):
        latest_sda_patient = self.latest_sda_patient()

        if latest_sda_patient is not None:
            return get_path(latest_sda_patient.data, 'name', 'given_name')
        else:
            return None

    @hybrid_property
    def last_name(self):
        latest_sda_patient = self.latest_sda_patient()

        if latest_sda_patient is not None:
            return get_path(latest_sda_patient.data, 'name', 'family_name')
        else:
            return None

    @hybrid_property
    def date_of_birth(self):
        latest_sda_patient = self.latest_sda_patient()

        if latest_sda_patient is not None:
            date_of_birth_str = get_path(latest_sda_patient.data, 'birth_time')

            if date_of_birth_str is None:
                return None
            else:
                try:
                    return datetime.strptime(date_of_birth_str, '%Y-%m-%dT%H:%M:%SZ')
                except ValueError:
                    return None
        else:
            return None

    @hybrid_property
    def gender(self):
        latest_sda_patient = self.latest_sda_patient()

        if latest_sda_patient is not None:
            return get_path(latest_sda_patient.data, 'gender', 'code')
        else:
            return None

    def latest_sda_patient(self):
        latest_sda_patient = None

        for sda_resource in self.sda_resources:
            sda_patient = sda_resource.sda_patient

            if sda_patient is None:
                continue

            # TODO choose last updated
            latest_sda_patient = sda_patient
            break

        return latest_sda_patient

    @first_name.expression
    def first_name(cls):
        patient_alias = aliased(Patient)

        # TODO choose last updated
        return select([SDAPatient.data[('name', 'given_name')].astext]) \
            .select_from(join(SDAPatient, SDAResource).join(patient_alias)) \
            .where(patient_alias.id == cls.id) \
            .as_scalar()

    @last_name.expression
    def last_name(cls):
        patient_alias = aliased(Patient)

        # TODO choose last updated
        return select([SDAPatient.data[('name', 'family_name')].astext]) \
            .select_from(join(SDAPatient, SDAResource).join(patient_alias)) \
            .where(patient_alias.id == cls.id) \
            .as_scalar()

    @date_of_birth.expression
    def date_of_birth(cls):
        patient_alias = aliased(Patient)

        # TODO choose last updated
        return select([SDAPatient.data['birth_time'].astext]) \
            .select_from(join(SDAPatient, SDAResource).join(patient_alias)) \
            .where(patient_alias.id == cls.id) \
            .as_scalar()

    @gender.expression
    def gender(cls):
        patient_alias = aliased(Patient)

        # TODO choose last updated
        return select([SDAPatient.data[('gender', 'code')].astext]) \
            .select_from(join(SDAPatient, SDAResource).join(patient_alias)) \
            .where(patient_alias.id == cls.id) \
            .as_scalar()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_admin = Column(Boolean, default=False, nullable=False)

    units = relationship('UnitUser')
    disease_groups = relationship('DiseaseGroupUser')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Unit(Base):
    __tablename__ = 'units'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    facility_id = Column(Integer, ForeignKey('facilities.id'))
    facility = relationship('Facility')

    patients = relationship('UnitPatient')
    users = relationship('UnitUser')


class DiseaseGroup(Base):
    __tablename__ = 'disease_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    patients = relationship('DiseaseGroupPatient')
    users = relationship('DiseaseGroupUser')
    features = relationship('DiseaseGroupFeatures', backref='disease_group')

    def has_feature(self, feature_name):
        return any(x.feature_name == feature_name for x in self.features)


class DiseaseGroupFeatures(Base):
    __tablename__ = 'disease_group_features'

    id = Column(Integer, primary_key=True)
    disease_group_id = Column(Integer, ForeignKey('disease_groups.id'))
    feature_name = Column(String, nullable=False)


class UnitPatient(Base):
    __tablename__ = 'unit_patients'

    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, ForeignKey('units.id'), nullable=False)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)

    unit = relationship('Unit')
    patient = relationship('Patient')

    __table_args__ = (
        UniqueConstraint('unit_id', 'patient_id'),
    )


class UnitUser(Base):
    __tablename__ = 'unit_users'

    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, ForeignKey('units.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role = Column(String, nullable=False)

    unit = relationship('Unit')
    user = relationship('User')

    __table_args__ = (
        UniqueConstraint('unit_id', 'user_id'),
    )


class DiseaseGroupPatient(Base):
    __tablename__ = 'disease_group_patients'

    id = Column(Integer, primary_key=True)
    disease_group_id = Column(Integer, ForeignKey('disease_groups.id'), nullable=False)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)

    disease_group = relationship('DiseaseGroup')
    patient = relationship('Patient')

    __table_args__ = (
        UniqueConstraint('disease_group_id', 'patient_id'),
    )


class DiseaseGroupUser(Base):
    __tablename__ = 'disease_group_users'

    id = Column(Integer, primary_key=True)
    disease_group_id = Column(Integer, ForeignKey('disease_groups.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role = Column(String, nullable=False)

    disease_group = relationship('DiseaseGroup')
    user = relationship('User')

    __table_args__ = (
        UniqueConstraint('disease_group_id', 'user_id'),
    )


class Facility(Base):
    __tablename__ = 'facilities'

    id = Column(Integer, primary_key=True)
    code = Column(Integer, unique=True)
    name = Column(String)


class SDAResource(Base):
    __tablename__ = 'sda_resources'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    facility = relationship('Facility')

    mpiid = Column(Integer)

    form = relationship('FormSDAResource', uselist=False)
    remote = relationship('RemoteSDAResource', uselist=False)

    sda_medications = relationship('SDAMedication', cascade='all')
    sda_patient = relationship('SDAPatient', uselist=False, cascade='all')


class SDAMedication(Base):
    __tablename__ = 'sda_medications'

    id = Column(Integer, primary_key=True)
    sda_resource_id = Column(Integer, ForeignKey('sda_resources.id'))
    sda_resource = relationship('SDAResource')

    data = Column(JSONB)


class SDAPatient(Base):
    __tablename__ = 'sda_patients'

    id = Column(Integer, primary_key=True)

    sda_resource_id = Column(Integer, ForeignKey('sda_resources.id'))
    sda_resource = relationship('SDAResource')

    data = Column(JSONB)

    aliases = relationship('SDAPatientAlias', cascade='all')
    numbers = relationship('SDAPatientNumber', cascade='all')
    addresses = relationship('SDAPatientAddress', cascade='all')


class SDAPatientAlias(Base):
    __tablename__ = 'sda_patient_aliases'

    id = Column(Integer, primary_key=True)

    sda_patient_id = Column(Integer, ForeignKey('sda_patients.id'))
    sda_patient = relationship('SDAPatient')

    data = Column(JSONB)


class SDAPatientNumber(Base):
    __tablename__ = 'sda_patient_numbers'

    id = Column(Integer, primary_key=True)

    sda_patient_id = Column(Integer, ForeignKey('sda_patients.id'))
    sda_patient = relationship('SDAPatient')

    data = Column(JSONB)


class SDAPatientAddress(Base):
    __tablename__ = 'sda_patient_addresses'

    id = Column(Integer, primary_key=True)

    sda_patient_id = Column(Integer, ForeignKey('sda_patients.id'))
    sda_patient = relationship('SDAPatient')

    data = Column(JSONB)

class FormSDAResource(Base):
    __tablename__ = 'form_sda_resources'

    form_id = Column(Integer, autoincrement=False)
    form_type = Column(String)
    sda_resource_id = Column(Integer, ForeignKey('sda_resources.id'))

    sda_resource = relationship('SDAResource')

    __table_args__ = (
        PrimaryKeyConstraint('form_id', 'form_type'),
    )

class RemoteSDAResource(Base):
    __tablename__ = 'remote_sda_resources'

    patient_id = Column(Integer, ForeignKey('patients.id'), primary_key=True)
    facility_id = Column(Integer, ForeignKey('facilities.id'), primary_key=True)
    sda_resource_id = Column(Integer, ForeignKey('sda_resources.id'), nullable=False)

    patient = relationship('Patient')
    facility = relationship('Facility')
    sda_resource = relationship('SDAResource')
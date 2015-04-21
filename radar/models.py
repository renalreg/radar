from sqlalchemy import Integer, Column, String, DateTime, ForeignKey, UniqueConstraint, select, join, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, aliased
from werkzeug.security import generate_password_hash, check_password_hash

from radar.database import Base


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)

    units = relationship('UnitPatient')
    disease_groups = relationship('DiseaseGroupPatient')
    sda_containers = relationship('SDAContainer', backref='patient')

    @hybrid_property
    def first_name(self):
        latest_sda_patient = self.latest_sda_patient()

        if latest_sda_patient is not None:
            return latest_sda_patient.name_given_name
        else:
            return None

    @hybrid_property
    def last_name(self):
        latest_sda_patient = self.latest_sda_patient()

        if latest_sda_patient is not None:
            return latest_sda_patient.name_family_name
        else:
            return None

    @hybrid_property
    def date_of_birth(self):
        latest_sda_patient = self.latest_sda_patient()

        if latest_sda_patient is not None:
            return latest_sda_patient.birth_time
        else:
            return None

    @hybrid_property
    def gender(self):
        latest_sda_patient = self.latest_sda_patient()

        if latest_sda_patient is not None:
            return latest_sda_patient.gender_code
        else:
            return None

    def latest_sda_patient(self):
        latest_sda_patient = None

        for sda_container in self.sda_containers:
            sda_patient = sda_container.sda_patient

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
        return select([SDAPatient.name_given_name])\
            .select_from(join(SDAPatient, SDAContainer).join(patient_alias))\
            .where(patient_alias.id == cls.id)\
            .as_scalar()

    @last_name.expression
    def last_name(cls):
        patient_alias = aliased(Patient)

        # TODO choose last updated
        return select([SDAPatient.name_family_name])\
            .select_from(join(SDAPatient, SDAContainer).join(patient_alias))\
            .where(patient_alias.id == cls.id)\
            .as_scalar()

    @date_of_birth.expression
    def date_of_birth(cls):
        patient_alias = aliased(Patient)

        # TODO choose last updated
        return select([SDAPatient.birth_time])\
            .select_from(join(SDAPatient, SDAContainer).join(patient_alias))\
            .where(patient_alias.id == cls.id)\
            .as_scalar()

    @gender.expression
    def gender(cls):
        patient_alias = aliased(Patient)

        # TODO choose last updated
        return select([SDAPatient.gender_code])\
            .select_from(join(SDAPatient, SDAContainer).join(patient_alias))\
            .where(patient_alias.id == cls.id)\
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

class SDAContainer(Base):
    __tablename__ = 'sda_containers'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)

    facility = relationship('Facility')
    sda_medications = relationship('SDAMedication', cascade='all, delete-orphan')
    sda_patient = relationship('SDAPatient', uselist=False, cascade='all, delete-orphan')

class SDAMedication(Base):
    __tablename__ = 'sda_medications'

    id = Column(Integer, primary_key=True)
    sda_container_id = Column(Integer, ForeignKey('sda_containers.id'))

    from_time = Column(DateTime)
    to_time = Column(DateTime)

class SDAPatient(Base):
    __tablename__ = 'sda_patients'

    id = Column(Integer, primary_key=True)

    sda_container_id = Column(Integer, ForeignKey('sda_containers.id'))
    sda_container = relationship('SDAContainer')

    name_name_prefix = Column(String)
    name_given_name = Column(String)
    name_middle_name = Column(String)
    name_family_name = Column(String)
    name_preferred_name = Column(String)

    gender_coding_standard = Column(String)
    gender_code = Column(String)
    gender_description = Column(String)

    birth_time = Column(DateTime)
    death_time = Column(DateTime)

    aliases = relationship('SDAPatientName')
    patient_numbers = relationship('SDAPatientNumber')

class SDAPatientName(Base):
    __tablename__ = 'sda_patient_names'

    id = Column(Integer, primary_key=True)

    sda_patient_id = Column(Integer, ForeignKey('sda_patients.id'))
    sda_patient = relationship('SDAPatient')

    name_prefix = Column(String)
    given_name = Column(String)
    middle_name = Column(String)
    family_name = Column(String)
    preferred_name = Column(String)

class SDAPatientNumber(Base):
    __tablename__ = 'sda_patient_numbers'

    id = Column(Integer, primary_key=True)

    sda_patient_id = Column(Integer, ForeignKey('sda_patients.id'))
    sda_patient = relationship('SDAPatient')

    number = Column(String)
    numberType = Column(String)
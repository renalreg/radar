from sqlalchemy import Integer, Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from radar.database import Base


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    units = relationship('UnitPatient')
    disease_groups = relationship('DiseaseGroupPatient')

    def filter_units_for_user(self, user):
        user_units = set([unit_user.unit_id for unit_user in user.units])

        # If the patient belongs to one of the user's units, the user can view all of the patient's units
        if any(unit_patient.unit_id in user_units for unit_patient in self.units):
            return list(self.units)
        else:
            return list()

    def filter_disease_groups_for_user(self, user):
        user_units = set([unit_user.unit_id for unit_user in user.units])

        # If the patient belongs to one of the user's units, the user can view all of the patient's disease groups
        if any(unit_patient.unit_id in user_units for unit_patient in self.units):
            return list(self.disease_groups)
        else:
            # Otherwise intersect the disease groups of the patient and the user
            user_disease_groups = set([dg_user.disease_group_id for dg_user in user.disease_groups])
            return [x for x in self.disease_groups if x.disease_group_id in user_disease_groups]

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)
    email = Column(String)

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

    def disease_groups_for_user(self, user):
        # TODO
        return self.disease_groups

    def units_for_user(self, user):
        # TODO
        return self.units

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
    sda_medications = relationship('SDAMedication', backref='sda_container', cascade='all, delete-orphan')

class SDAMedication(Base):
    __tablename__ = 'sda_medications'

    id = Column(Integer, primary_key=True)
    sda_container_id = Column(Integer, ForeignKey('sda_containers.id'))
    from_time = Column(DateTime)
    to_time = Column(DateTime)

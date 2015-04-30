from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from radar.users.roles import DISEASE_GROUP_VIEW_PATIENT_ROLES, \
    DISEASE_GROUP_VIEW_DEMOGRAPHICS_ROLES, UNIT_VIEW_DEMOGRAPHICS_ROLES, UNIT_VIEW_PATIENT_ROLES, \
    DISEASE_GROUP_VIEW_USER_ROLES, UNIT_VIEW_USER_ROLES, UNIT_EDIT_PATIENT_ROLES
from radar.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_admin = Column(Boolean, default=False, nullable=False)

    unit_users = relationship('UnitUser', back_populates='user')
    disease_group_users = relationship('DiseaseGroupUser', back_populates='user')

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

    def has_view_patient_permission(self):
        return (
            self.is_admin or
            any(x.has_view_patient_permission() for x in self.disease_groups) or
            any(x.has_view_patient_permission() for x in self.units)
        )

    def has_view_demographics_permission(self):
        return (
            self.is_admin or
            any(x.has_demographics_permission() for x in self.disease_groups) or
            any(x.has_demographics_permission() for x in self.units)
        )

    @property
    def units(self):
        return [x.unit for x in self.unit_users]

    @property
    def disease_groups(self):
        return [x.disease_group for x in self.disease_group_users]


class DiseaseGroupUser(db.Model):
    __tablename__ = 'disease_group_users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    disease_group_id = Column(Integer, ForeignKey('disease_groups.id'), nullable=False)
    role = Column(String, nullable=False)

    user = relationship('User')
    disease_group = relationship('DiseaseGroup')

    __table_args__ = (
        UniqueConstraint('disease_group_id', 'user_id'),
    )

    @property
    def has_view_demographics_permission(self):
        return self.role in DISEASE_GROUP_VIEW_DEMOGRAPHICS_ROLES

    @property
    def has_view_patient_permission(self):
        return self.role in DISEASE_GROUP_VIEW_PATIENT_ROLES

    @property
    def has_view_user_permission(self):
        return self.role in DISEASE_GROUP_VIEW_USER_ROLES


class UnitUser(db.Model):
    __tablename__ = 'unit_users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    unit_id = Column(Integer, ForeignKey('units.id'), nullable=False)
    role = Column(String, nullable=False)

    unit = relationship('Unit')
    user = relationship('User')

    __table_args__ = (
        UniqueConstraint('unit_id', 'user_id'),
    )

    @property
    def has_view_demographics_permission(self):
        return self.role in UNIT_VIEW_DEMOGRAPHICS_ROLES

    @property
    def has_view_patient_permission(self):
        return self.role in UNIT_VIEW_PATIENT_ROLES

    @property
    def has_view_patient_permission(self):
        return self.role in UNIT_EDIT_PATIENT_ROLES

    @property
    def has_view_user_permission(self):
        return self.role in UNIT_VIEW_USER_ROLES
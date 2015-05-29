from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, select, Date, DateTime, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, aliased

from radar.lib.database import db
from radar.models.common import DataSource, MetadataMixin, PatientMixin


class Patient(db.Model):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)

    recruited_user_id = Column(Integer, ForeignKey('users.id'))
    recruited_date = Column(DateTime(timezone=False), default=datetime.now)
    recruited_unit_id = Column(Integer, ForeignKey('units.id'))

    recruited_user = relationship('User')
    recruited_unit = relationship('Unit')

    is_active = Column(Boolean, nullable=False, default=True, server_default='1')

    units = relationship('UnitPatient')
    disease_groups = relationship('DiseaseGroupPatient')

    demographics = relationship('PatientDemographics')
    numbers = relationship('PatientNumber')
    alias = relationship('PatientAlias')

    def latest_demographics_attr(self, attr):
        demographics = self.latest_demographics

        if demographics is None:
            return None

        return getattr(demographics, attr)

    @classmethod
    def latest_demographics_query(cls, column):
        patient_alias = aliased(Patient)

        return select([column])\
            .select_from(PatientDemographics.join(patient_alias))\
            .where(patient_alias.id == cls.id)\
            .order_by(PatientDemographics.modified_at)\
            .limit(1)\
            .as_scalar()

    @property
    def latest_demographics(self):
        demographics_list = self.demographics

        if len(demographics_list) == 0:
            return None

        def latest(x):
            return x.modified_at or datetime.min

        return min(demographics_list, key=latest)

    @hybrid_property
    def first_name(self):
        return self.latest_demographics_attr('first_name')

    @hybrid_property
    def last_name(self):
        return self.latest_demographics_attr('last_name')

    @hybrid_property
    def date_of_birth(self):
        return self.latest_demographics_attr('date_of_birth')

    @hybrid_property
    def gender(self):
        return self.latest_demographics_attr('gender')

    @hybrid_property
    def is_male(self):
        return self.gender == 'M'

    @hybrid_property
    def is_female(self):
        return self.gender == 'F'

    @first_name.expression
    def first_name(cls):
        return cls.latest_demographics_query(PatientDemographics.first_name)

    @last_name.expression
    def last_name(cls):
        return cls.latest_demographics_query(PatientDemographics.last_name)

    @date_of_birth.expression
    def date_of_birth(cls):
        return cls.latest_demographics_query(PatientDemographics.date_of_birth)

    @gender.expression
    def gender(cls):
        return cls.latest_demographics_query(PatientDemographics.gender)

    def _has_unit_permission(self, user, permission):
        patient_units = set([x.unit for x in self.units])

        for unit_user in user.units:
            if getattr(unit_user, 'has_' + permission + '_permission') and unit_user.unit in patient_units:
                return True

        return False

    def _has_disease_group_permission(self, user, permission):
        patient_disease_groups = set([x.disease_group for x in self.disease_groups])

        for disease_group_user in user.disease_groups:
            if getattr(disease_group_user, 'has_' + permission + '_permission') and\
                            disease_group_user.disease_group in patient_disease_groups:
                return True

        return False

    def can_view(self, user):
        return (
            user.is_admin or
            self._has_unit_permission(user, 'view_patient') or
            self._has_disease_group_permission(user, 'view_patient')
        )

    def can_edit(self, user):
        return (
           user.is_admin or
           self._has_unit_permission(user, 'edit_patient')
        )

    def can_view_demographics(self, user):
        if user.is_admin:
            return True

        if self._has_unit_permission(user, 'view_demographics'):
            return True

        if self._has_disease_group_permission(user, 'view_demographics'):
            return True

        return False

    def filter_units_for_user(self, user):
        """ Patient units a user can view """

        _ = user
        return self.units

    def filter_disease_groups_for_user(self, user):
        """ Patient disease groups a user can view """

        # The user can view all of the patient's disease groups if:
        # * The user is an admin
        # * The patient belongs to one of the user's units
        if user.is_admin or self._has_unit_permission(user, 'view_patient'):
            return self.disease_groups
        else:
            # Otherwise intersect the disease groups of the patient and the user
            user_disease_groups = set([x.disease_group for x in user.disease_groups])
            common_disease_groups = [x for x in self.disease_groups if x.disease_group in user_disease_groups]
            return common_disease_groups

    def available_units_for_user(self, user):
        """ Patient units that a user can save data under """

        # TODO intersect patient units with user units with write permissions
        return self.units

    def in_disease_group(self, disease_group):
        # TODO
        return False

    def in_unit(self, unit):
        # TODO
        return False


class PatientDemographics(db.Model, MetadataMixin):
    __tablename__ = 'patient_demographics'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    facility = relationship('Facility')

    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    date_of_death = Column(Date)
    gender = Column(Integer)

    # TODO
    ethnicity = Column(String)

    address_line_1 = Column(String)
    address_line_2 = Column(String)
    address_line_3 = Column(String)
    postcode = Column(String)

    home_number = Column(String)
    work_number = Column(String)
    mobile_number = Column(String)
    email_address = Column(String)

    nhs_no = Column(Integer)
    chi_no = Column(Integer)

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user) and self.patient.can_view(user)


class PatientAlias(db.Model, MetadataMixin):
    __tablename__ = 'patient_aliases'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    facility = relationship('Facility')

    first_name = Column(String)
    last_name = Column(String)

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user) and self.patient.can_view(user)


class PatientAddress(db.Model, MetadataMixin):
    __tablename__ = 'patient_addresses'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    facility = relationship('Facility')

    from_date = Column(Date)
    to_date = Column(Date)
    address_line_1 = Column(String)
    address_line_2 = Column(String)
    address_line_3 = Column(String)
    postcode = Column(String)

    @property
    def full_address(self):
        parts = []

        parts.extend([
            self.address_line_1,
            self.address_line_2,
            self.address_line_3,
            self.postcode,
        ])

        return "\n".join(x for x in parts if x)

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user) and self.patient.can_view(user)


class PatientNumber(db.Model, MetadataMixin):
    __tablename__ = 'patient_numbers'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    facility = relationship('Facility', foreign_keys=[facility_id])

    number_facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    number_facility = relationship('Facility', foreign_keys=[number_facility_id])

    number = Column(String, nullable=False)

    def can_view(self, user):
        return self.patient.can_view(user)

    def can_edit(self, user):
        return self.patient.can_edit(user) and self.patient.can_view(user)
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, select, join, Date, DateTime, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, aliased

from radar.lib.database import db
from radar.models.base import DataSource, CreatedModifiedMixin, PatientMixin
from radar.lib.sda.models import SDAPatient, SDABundle


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

    sda_bundles = relationship('SDABundle', passive_deletes=True)

    def _latest_sda_patient_attr(self, attr):
        sda_patient = self.latest_sda_patient

        if sda_patient is None:
            return None

        return getattr(sda_patient, attr)

    @classmethod
    def _latest_sda_patient_query(cls, column):
        patient_alias = aliased(Patient)

        # TODO last updated
        return select([column])\
            .select_from(join(SDAPatient, SDABundle).join(patient_alias))\
            .where(patient_alias.id == cls.id)\
            .limit(1)\
            .as_scalar()

    @property
    def latest_sda_patient(self):
        latest_sda_patient = None

        for sda_bundle in self.sda_bundles:
            sda_patient = sda_bundle.sda_patient

            if sda_patient is None:
                continue

            # TODO last updated
            latest_sda_patient = sda_patient
            break

        return latest_sda_patient

    @hybrid_property
    def first_name(self):
        return self._latest_sda_patient_attr('first_name')

    @hybrid_property
    def last_name(self):
        return self._latest_sda_patient_attr('last_name')

    @hybrid_property
    def date_of_birth(self):
        return self._latest_sda_patient_attr('date_of_birth')

    @hybrid_property
    def gender(self):
        return self._latest_sda_patient_attr('gender')

    @hybrid_property
    def is_male(self):
        return self.gender == 'M'

    @hybrid_property
    def is_female(self):
        return self.gender == 'F'

    @first_name.expression
    def first_name(cls):
        return cls._latest_sda_patient_query(SDAPatient.first_name)

    @last_name.expression
    def last_name(cls):
        return cls._latest_sda_patient_query(SDAPatient.last_name)

    @date_of_birth.expression
    def date_of_birth(cls):
        return cls._latest_sda_patient_query(SDAPatient.date_of_birth)

    @gender.expression
    def gender(cls):
        return cls._latest_sda_patient_query(SDAPatient.gender)

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


class Demographics(DataSource, PatientMixin, CreatedModifiedMixin):
    __tablename__ = 'demographics'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)

    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    date_of_death = Column(Date)
    gender = Column(Integer)

    # TODO
    ethnicity = Column(String)

    alias_first_name = Column(String)
    alias_last_name = Column(String)

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

    __mapper_args__ = {
        'polymorphic_identity': 'demographics',
    }

    def can_view(self, user):
        return self.patient.can_view_demographics(user)

    def can_edit(self, user):
        return self.patient.can_edit(user) and self.patient.can_view_demographics(user)
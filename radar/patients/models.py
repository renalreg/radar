from sqlalchemy import Column, Integer, ForeignKey, String, select, join
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, aliased
from radar.database import db
from radar.models import DataSource
from radar.sda.models import SDAPatient, SDAResource


class Patient(db.Model):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)

    units = relationship('UnitPatient')
    disease_groups = relationship('DiseaseGroupPatient')

    sda_resources = relationship('SDAResource')

    def _latest_sda_patient_attr(self, attr):
        sda_patient = self.latest_sda_patient

        if sda_patient is None:
            return None

        return getattr(sda_patient, attr)

    @classmethod
    def _latest_sda_patient_query(cls, column):
        patient_alias = aliased(Patient)

        # TODO last updated
        return select([column]) \
            .select_from(join(SDAPatient, SDAResource).join(patient_alias)) \
            .where(patient_alias.id == cls.id) \
            .as_scalar()

    @property
    def latest_sda_patient(self):
        latest_sda_patient = None

        for sda_resource in self.sda_resources:
            sda_patient = sda_resource.sda_patient

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
                            disease_group_user.unit in patient_disease_groups:
                return True

        return False

    def can_view(self, user):
        if user.is_admin:
            return True

        if self._has_unit_permission(user, 'view_patient'):
            return True

        if self._has_disease_group_permission(user, 'view_patient'):
            return True

        return False

    def can_view_demographics(self, user):
        if user.is_admin:
            return True

        if self._has_unit_permission(user, 'view_demographics'):
            return True

        if self._has_disease_group_permission(user, 'view_demographics'):
            return True

        return False

    def filter_units_for_user(self, user):
        _ = user
        return self.units

    def filter_disease_groups_for_user(self, user):
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

class Demographics(DataSource):
    __tablename__ = 'demographics'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship('Patient')

    first_name = Column(String)
    last_name = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'demographics',
    }
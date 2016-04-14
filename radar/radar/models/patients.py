from collections import OrderedDict
from datetime import datetime
from sqlalchemy import Column, Integer, select, join, String, func, exists, Sequence

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import aliased
from radar.database import db
from radar.models.common import MetaModelMixin
from radar.models.patient_demographics import PatientDemographics
from radar.models.patient_numbers import PatientNumber
from radar.models.groups import Group, GroupPatient, GROUP_TYPE, GROUP_CODE_RADAR
from radar.groups import is_radar_group
from radar.models.logs import log_changes
from radar.utils import seconds_to_age

GENDER_NOT_KNOWN = 0
GENDER_MALE = 1
GENDER_FEMALE = 2
GENDER_NOT_SPECIFIED = 9

GENDERS = OrderedDict([
    (GENDER_NOT_KNOWN, 'Not Known'),
    (GENDER_MALE, 'Male'),
    (GENDER_FEMALE, 'Female'),
    (GENDER_NOT_SPECIFIED, 'Not Specified'),
])

ETHNICITIES = OrderedDict([
    ('A', 'White - British'),
    ('B', 'White - Irish'),
    ('C', 'Other White Background'),
    ('D', 'Mixed - White and Black Caribbean'),
    ('E', 'Mixed - White and Black African'),
    ('F', 'Mixed - White and Asian'),
    ('G', 'Other Mixed Background'),
    ('H', 'Asian or Asian British - Indian'),
    ('J', 'Asian or Asian British - Pakistani'),
    ('K', 'Asian or Asian British - Bangladeshi'),
    ('L', 'Other Asian Background'),
    ('M', 'Black Carribean'),
    ('N', 'Black African'),
    ('P', 'Other Black Background'),
    ('R', 'Chinese'),
    ('S', 'Other Ethnic Background'),
    ('Z', 'Refused / Not Stated'),
])


@log_changes
class Patient(db.Model, MetaModelMixin):
    __tablename__ = 'patients'

    id = Column(Integer, Sequence('patients_seq'), primary_key=True)
    comments = Column(String)

    @property
    def groups(self):
        return [x.group for x in self.group_patients]

    @property
    def current_groups(self):
        return [x.group for x in self.current_group_patients]

    @property
    def current_group_patients(self):
        return [x for x in self.group_patients if x.current]

    @hybrid_property
    def recruited_date(self):
        from_dates = [x.from_date for x in self.group_patients if is_radar_group(x.group)]

        if from_dates:
            return max(from_dates)
        else:
            return None

    @recruited_date.expression
    def recruited_date(cls):
        return select([func.min(GroupPatient.from_date)])\
            .select_from(join(GroupPatient, Group, GroupPatient.group_id == Group.id))\
            .where(GroupPatient.patient_id == cls.id)\
            .where(Group.code == GROUP_CODE_RADAR)\
            .where(Group.type == GROUP_TYPE.OTHER)\
            .as_scalar()

    @hybrid_property
    def current(self):
        return any(is_radar_group(x) for x in self.current_groups)

    @current.expression
    def current(cls):
        q = exists()
        q = q.select_from(join(GroupPatient, Group, GroupPatient.group_id == Group.id))
        q = q.where(GroupPatient.patient_id == cls.id)
        q = q.where(GroupPatient.current == True)  # noqa
        q = q.where(Group.code == GROUP_CODE_RADAR)
        q = q.where(Group.type == GROUP_TYPE.OTHER)
        return q

    @property
    def _recruited_group_patient(self):
        from_date = None
        recruited_group_patient = None

        for group_patient in self.group_patients:
            if (
                is_radar_group(group_patient.group) and
                (
                    from_date is None or
                    group_patient.from_date < from_date
                )
            ):
                from_date = group_patient.from_date
                recruited_group_patient = group_patient

        return recruited_group_patient

    @property
    def recruited_user(self):
        group_patient = self._recruited_group_patient

        if group_patient is None:
            user = None
        else:
            user = group_patient.created_user

        return user

    @property
    def recruited_group(self):
        group_patient = self._recruited_group_patient

        if group_patient is None:
            group = None
        else:
            group = group_patient.created_group

        return group

    @property
    def primary_patient_number(self):
        patient_numbers = [x for x in self.patient_numbers if x.number_group.is_recruitment_number_group]

        if len(patient_numbers) == 0:
            return None

        def by_modified_date(x):
            return (x.modified_date or datetime.min, x.id)

        return max(patient_numbers, key=by_modified_date)

    @hybrid_property
    def primary_patient_number_number(self):
        patient_number = self.primary_patient_number

        if patient_number is None:
            return None
        else:
            return patient_number.number

    @primary_patient_number_number.expression
    def primary_patient_number_number(cls):
        patient_alias = aliased(Patient)

        return (
            select([PatientNumber.number])
            .select_from(join(PatientNumber, patient_alias).join(Group, PatientNumber.number_group_id == Group.id))
            .where(patient_alias.id == cls.id)
            .where(Group.is_recruitment_number_group == True)  # noqa
            .order_by(
                PatientNumber.modified_date.desc(),
                PatientNumber.id.desc(),
            )
            .limit(1)
            .as_scalar()
        )

    def latest_demographics_attr(self, attr):
        demographics = self.latest_demographics

        if demographics is None:
            return None

        return getattr(demographics, attr)

    @classmethod
    def latest_demographics_query(cls, column):
        patient_alias = aliased(Patient)

        return select([column])\
            .select_from(join(PatientDemographics, patient_alias))\
            .where(patient_alias.id == cls.id)\
            .order_by(
                PatientDemographics.modified_date.desc(),
                PatientDemographics.id.desc(),
            )\
            .limit(1)\
            .as_scalar()

    @property
    def latest_demographics(self):
        patient_demographics = self.patient_demographics

        if len(patient_demographics) == 0:
            return None

        def by_modified_date(x):
            return (x.modified_date or datetime.min, x.id)

        return max(patient_demographics, key=by_modified_date)

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
    def date_of_death(self):
        return self.latest_demographics_attr('date_of_death')

    @hybrid_property
    def ethnicity(self):
        return self.latest_demographics_attr('ethnicity')

    @hybrid_property
    def gender(self):
        return self.latest_demographics_attr('gender')

    @hybrid_property
    def home_number(self):
        return self.latest_demographics_attr('home_number')

    @hybrid_property
    def work_number(self):
        return self.latest_demographics_attr('work_number')

    @hybrid_property
    def mobile_number(self):
        return self.latest_demographics_attr('mobile_number')

    @hybrid_property
    def email_address(self):
        return self.latest_demographics_attr('email_address')

    @hybrid_property
    def is_male(self):
        return self.gender == GENDER_MALE

    @hybrid_property
    def is_female(self):
        return self.gender == GENDER_FEMALE

    @first_name.expression
    def first_name(cls):
        return cls.latest_demographics_query(PatientDemographics.first_name)

    @last_name.expression
    def last_name(cls):
        return cls.latest_demographics_query(PatientDemographics.last_name)

    @date_of_birth.expression
    def date_of_birth(cls):
        return cls.latest_demographics_query(PatientDemographics.date_of_birth)

    @date_of_death.expression
    def date_of_death(cls):
        return cls.latest_demographics_query(PatientDemographics.date_of_death)

    @ethnicity.expression
    def ethnicity(cls):
        return cls.latest_demographics_query(PatientDemographics.ethnicity)

    @gender.expression
    def gender(cls):
        return cls.latest_demographics_query(PatientDemographics.gender)

    @home_number.expression
    def home_number(cls):
        return cls.latest_demographics_query(PatientDemographics.home_number)

    @work_number.expression
    def work_number(cls):
        return cls.latest_demographics_query(PatientDemographics.work_number)

    @mobile_number.expression
    def mobile_number(cls):
        return cls.latest_demographics_query(PatientDemographics.mobile_number)

    @email_address.expression
    def email_address(cls):
        return cls.latest_demographics_query(PatientDemographics.email_address)

    @property
    def earliest_date_of_birth(self):
        earliest_date_of_birth = None

        for demographics in self.patient_demographics:
            date_of_birth = demographics.date_of_birth

            if date_of_birth is not None and (earliest_date_of_birth is None or date_of_birth < earliest_date_of_birth):
                earliest_date_of_birth = date_of_birth

        return earliest_date_of_birth

    def in_group(self, group, current=None):
        if current is None:
            return any(x == group for x in self.groups)
        elif current:
            return any(x == group for x in self.current_groups)
        else:
            # TODO search historic groups
            raise NotImplementedError()

    @property
    def first_names(self):
        # TODO unique
        values = [x.first_name for x in self.patient_demographics]
        values.extend(x.first_name for x in self.patient_aliases)
        values = [x.upper() for x in values if x]
        return values

    @property
    def last_names(self):
        # TODO unique
        values = [x.last_name for x in self.patient_demographics]
        values.extend(x.last_name for x in self.patient_aliases)
        values = [x.upper() for x in values if x]
        return values

    @property
    def date_of_births(self):
        # TODO unique
        values = [x.date_of_birth for x in self.patient_demographics]
        values = [x for x in values if x]
        return values

    def to_age(self, date):
        date_of_birth = self.date_of_birth

        if date_of_birth is None:
            seconds = None
        else:
            seconds = (date - date_of_birth).total_seconds()
            seconds = seconds_to_age(seconds)

        return seconds

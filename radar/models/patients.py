from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, exists, func, Integer, join, select, Sequence, String, text
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import aliased

from radar.database import db
from radar.models.common import MetaModelMixin
from radar.models.diagnoses import GROUP_DIAGNOSIS_TYPE
from radar.models.groups import Group, GROUP_TYPE, GroupPatient
from radar.models.logs import log_changes
from radar.models.patient_codes import ETHNICITIES, GENDER_FEMALE, GENDER_MALE, GENDERS
from radar.models.patient_demographics import PatientDemographics
from radar.models.patient_numbers import PatientNumber
from radar.models.source_types import SOURCE_TYPE_MANUAL
from radar.utils import months_between, round_age, uniq


SIXTEEN_YEARS_IN_MONTHS = 12 * 16
EIGHTEEN_YEARS_IN_MONTHS = 12 * 18


class CONSENT_STATUS(Enum):
    """Enum for possible patient status in regards to consents.

    OK - means patient is consented, nothing needs to be done.
    SOON - patient is consented, but consent is coming to an end.
           Usually that means that patient has been consented as a
           child and now is coming to adulthood and needs to be
           reconsented as an adult.
    EXPIRED - consent is not valid anymore and patient should be
              frozen.
    MISSING - patient was not consented.
    """
    OK = 'OK'
    SOON = 'SOON'
    EXPIRED = 'EXPIRED'
    MISSING = 'MISSING'

    def __str__(self):
        return str(self.value)


def clean(items):
    return uniq(x for x in items if x)


@log_changes
class Patient(db.Model, MetaModelMixin):
    __tablename__ = 'patients'

    id = Column(Integer, Sequence('patients_seq'), primary_key=True)
    comments = Column(String)
    test = Column(Boolean, default=False, nullable=False, server_default=text('false'))
    control = Column(Boolean, default=False, nullable=False, server_default=text('false'))
    signed_off = Column(Boolean, default=False, nullable=False, server_default=text('false'))

    @property
    def cohorts(self):
        """Return cohorts that patient belongs to."""
        return [group for group in self.groups if group.type == GROUP_TYPE.COHORT]

    @property
    def systems(self):
        """Return groups of type GROUP_TYPE.SYSTEM that patient belongs to."""
        return [group for group in self.groups if group.type == GROUP_TYPE.SYSTEM]

    @property
    def hospitals(self):
        """Return groups of type GROUP_TYPE.HOSPITAL that patient belongs to."""
        return [group for group in self.groups if group.type == GROUP_TYPE.HOSPITAL]

    @property
    def groups(self):
        return [x.group for x in self.group_patients]

    @property
    def current_groups(self):
        return [x.group for x in self.current_group_patients]

    @property
    def current_group_patients(self):
        return [x for x in self.group_patients if x.current]

    @hybrid_method
    def recruited_date(self, group=None):
        group_patient = self._recruited_group_patient(group)

        if group_patient is None:
            from_date = None
        else:
            from_date = group_patient.from_date

        return from_date

    @recruited_date.expression
    def recruited_date(cls, group=None):
        q = select([func.min(GroupPatient.from_date)])
        q = q.select_from(join(GroupPatient, Group, GroupPatient.group_id == Group.id))
        q = q.where(GroupPatient.patient_id == cls.id)

        if group is not None:
            q = q.where(Group.id == group.id)
        else:
            q = q.where(Group.type == GROUP_TYPE.SYSTEM)

        q = q.as_scalar()

        return q

    @hybrid_method
    def current(self, group=None):
        if group is not None:
            return group in self.current_groups
        else:
            return any(group.type == GROUP_TYPE.SYSTEM for group in self.current_groups)

    @current.expression
    def current(cls, group=None):
        q = exists()
        q = q.select_from(join(GroupPatient, Group, GroupPatient.group_id == Group.id))
        q = q.where(GroupPatient.patient_id == cls.id)
        q = q.where(GroupPatient.current == True)  # noqa

        if group is not None:
            q = q.where(Group.id == group.id)
        else:
            q = q.where(Group.type == GROUP_TYPE.SYSTEM)

        return q

    def _recruited_group_patient(self, group=None):
        from_date = None
        recruited_group_patient = None

        for group_patient in self.group_patients:
            if (
                (
                    (group is not None and group_patient.group == group) or
                    (group is None and group_patient.group.type == GROUP_TYPE.SYSTEM)
                ) and
                (
                    from_date is None or
                    group_patient.from_date < from_date
                )
            ):
                from_date = group_patient.from_date
                recruited_group_patient = group_patient

        return recruited_group_patient

    def recruited_user(self, group=None):
        group_patient = self._recruited_group_patient(group)

        if group_patient is None:
            user = None
        else:
            user = group_patient.created_user

        return user

    def recruited_group(self, group=None):
        group_patient = self._recruited_group_patient(group)

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

    def latest_demographics_attr(self, attr, radar_only=False):
        demographics = self.latest_demographics(radar_only)

        if demographics is None:
            return None

        return getattr(demographics, attr)

    @classmethod
    def latest_demographics_query(cls, column):
        patient_alias = aliased(Patient)

        return (
            select([column])
            .select_from(join(PatientDemographics, patient_alias))
            .where(patient_alias.id == cls.id)
            .order_by(
                PatientDemographics.modified_date.desc(),
                PatientDemographics.id.desc(),
            )
            .limit(1)
            .as_scalar()
        )

    def latest_demographics(self, radar_only):
        patient_demographics = self.patient_demographics

        if len(patient_demographics) == 0:
            return None

        def by_modified_date(x):
            return (x.modified_date or datetime.min, x.id)

        def filter_radar_only(x):
            return x.source_type == SOURCE_TYPE_MANUAL

        if radar_only:
            patient_demographics = filter(filter_radar_only, patient_demographics)

        return max(patient_demographics, key=by_modified_date)

    @property
    def available_ethnicity(self):
        ethnicities = [demog.ethnicity for demog in self.patient_demographics]
        first_available = next((ethn for ethn in ethnicities if ethn is not None), None)
        return first_available

    @hybrid_property
    def first_name(self):
        return self.latest_demographics_attr('first_name')

    @property
    def radar_first_name(self):
        return self.latest_demographics_attr('first_name', radar_only=True)

    @hybrid_property
    def last_name(self):
        return self.latest_demographics_attr('last_name')

    @property
    def radar_last_name(self):
        return self.latest_demographics_attr('last_name', radar_only=True)

    @property
    def full_name(self):
        first_name = self.first_name
        last_name = self.last_name
        if not first_name:
            return last_name
        if not last_name:
            return first_name
        return '{} {}'.format(first_name, last_name)

    @hybrid_property
    def date_of_birth(self):
        return self.latest_demographics_attr('date_of_birth')

    @property
    def radar_date_of_birth(self):
        return self.latest_demographics_attr('date_of_birth', radar_only=True)

    @property
    def year_of_birth(self):
        date_of_birth = self.date_of_birth

        if date_of_birth is None:
            year_of_birth = None
        else:
            year_of_birth = date_of_birth.year

        return year_of_birth

    @hybrid_property
    def date_of_death(self):
        return self.latest_demographics_attr('date_of_death')

    @property
    def radar_date_of_death(self):
        return self.latest_demographics_attr('date_of_death', radar_only=True)

    @property
    def year_of_death(self):
        date_of_death = self.date_of_death

        if date_of_death is None:
            year_of_death = None
        else:
            year_of_death = date_of_death.year

        return year_of_death

    @hybrid_property
    def nationality(self):
        return self.latest_demographics_attr('nationality')

    @hybrid_property
    def ethnicity(self):
        return self.latest_demographics_attr('ethnicity')

    @property
    def radar_ethnicity(self):
        return self.latest_demographics_attr('ethnicity', radar_only=True)

    @hybrid_property
    def gender(self):
        return self.latest_demographics_attr('gender')

    @property
    def radar_gender(self):
        return self.latest_demographics_attr('gender', radar_only=True)

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
        values = [x.first_name for x in self.patient_demographics]
        values += [x.first_name for x in self.patient_aliases]
        values = clean(values)
        return values

    @property
    def last_names(self):
        values = [x.last_name for x in self.patient_demographics]
        values += [x.last_name for x in self.patient_aliases]
        values = clean(values)
        return values

    @property
    def dates_of_birth(self):
        values = [x.date_of_birth for x in self.patient_demographics]
        values = clean(values)
        return values

    @property
    def genders(self):
        values = [x.gender for x in self.patient_demographics]
        values = clean(values)
        return values

    def to_age(self, date):
        """Months between date of birth and supplied date."""

        date_of_birth = self.date_of_birth

        if date_of_birth is None:
            months = None
        else:
            months = round_age(months_between(date, date_of_birth))

        return months

    @property
    def frozen(self):
        """True if the patient is frozen."""
        return not self.current

    @hybrid_property
    def ukrdc(self):
        """True if the patient is receiving data from the UKRDC."""
        return self.ukrdc_patient is not None

    @ukrdc.expression
    def ukrdc(cls):
        return cls.ukrdc_patient.has()

    @property
    def gender_label(self):
        return GENDERS.get(self.gender)

    @property
    def ethnicity_label(self):
        return ETHNICITIES.get(self.ethnicity)

    @property
    def consented(self):
        return bool(self.consents)

    @property
    def paediatric(self):
        """Return true if patient is less than 16 years old."""
        months = self.to_age(datetime.now().date())
        if months:
            years_old = months // 12
            return years_old < 16
        return False

    def recruited_paediatric(self):
        """Return whether patient was recruited as paediatric."""
        months = self.to_age(self.recruited_date())
        if months and months < SIXTEEN_YEARS_IN_MONTHS:
            return True
        return False

    @property
    def youth(self):
        """Return true if patient is [16-18) years old."""
        months = self.to_age(datetime.now().date())
        if months:
            years_old = months // 12
            return 16 <= years_old < 18
        return False

    @property
    def adult(self):
        """Return true if patient is 18 years or older."""
        return not self.paediatric and not self.youth

    @property
    def consent_status(self):
        """Return what consent status patient is in."""
        if self.year_of_death:
            return CONSENT_STATUS.OK

        if len(self.consents) == 0:
            return CONSENT_STATUS.MISSING

        old = False
        if len(self.consents) == 1 and self.consents[0].consent.code == 'old':
            old = True

        if self.paediatric and old:
            return CONSENT_STATUS.EXPIRED
        elif self.youth and old:
            return CONSENT_STATUS.SOON
        elif old:
            return CONSENT_STATUS.EXPIRED

        paediatric_consent = False
        new_consent = False
        old_consent = False
        for patient_consent in self.consents:
            consent = patient_consent.consent
            if consent.paediatric:
                paediatric_consent = True
            elif consent.code != 'old':
                new_consent = True
            else:
                old_consent = True

        if paediatric_consent and self.adult and not new_consent:
            return CONSENT_STATUS.EXPIRED

        if paediatric_consent and self.youth and not new_consent:
            return CONSENT_STATUS.SOON

        if old_consent and not new_consent and not paediatric_consent:
            return CONSENT_STATUS.EXPIRED

        return CONSENT_STATUS.OK

    def primary_diagnosis(self, cohort):
        """
        Return primary diagnosis in a cohort, or None if it is not
        yet added.
        """
        primary_diagnoses = [
            group_diagnosis.diagnosis
            for group_diagnosis in cohort.group_diagnoses
            if group_diagnosis.type == GROUP_DIAGNOSIS_TYPE.PRIMARY
        ]

        for patient_diagnosis in self.patient_diagnoses:
            if patient_diagnosis.diagnosis in primary_diagnoses:
                return patient_diagnosis

        return None

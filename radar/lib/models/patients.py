from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, select, Date, DateTime, Boolean, join, \
    UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, aliased

from radar.lib.database import db
from radar.lib.models.common import MetaModelMixin, StringLookupTable


class Patient(db.Model):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)

    # TODO move
    recruited_user_id = Column(Integer, ForeignKey('users.id'))
    recruited_user = relationship('User')
    recruited_date = Column(DateTime(timezone=False), default=datetime.now)
    recruited_organisation_id = Column(Integer, ForeignKey('organisations.id'))
    recruited_organisation = relationship('Organisation')

    is_active = Column(Boolean, nullable=False, default=True, server_default='1')

    organisation_patients = relationship('OrganisationPatient')
    cohort_patients = relationship('CohortPatient')

    patient_demographics = relationship('PatientDemographics')
    patient_numbers = relationship('PatientNumber')
    patient_aliases = relationship('PatientAlias')

    @property
    def organisations(self):
        return [x.organisation for x in self.organisation_patients]

    @property
    def disease_groups(self):
        return [x.cohort for x in self.disease_group_patients]

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
            .order_by(PatientDemographics.modified_date.desc())\
            .limit(1)\
            .as_scalar()

    @property
    def latest_demographics(self):
        patient_demographics = self.patient_demographics

        if len(patient_demographics) == 0:
            return None

        def by_modified_date(x):
            return x.modified_date or datetime.min

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

    @property
    def earliest_date_of_birth(self):
        earliest_date_of_birth = None

        for demographics in self.patient_demographics:
            date_of_birth = demographics.date_of_birth
            if date_of_birth is not None and (earliest_date_of_birth is None or date_of_birth < earliest_date_of_birth):
                earliest_date_of_birth = date_of_birth

        return earliest_date_of_birth


class PatientDemographics(db.Model, MetaModelMixin):
    __tablename__ = 'patient_demographics'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    date_of_death = Column(Date)
    gender = Column(String)

    ethnicity_code_id = Column(String, ForeignKey('ethnicity_codes.id'))
    ethnicity_code = relationship('EthnicityCode')

    home_number = Column(String)
    work_number = Column(String)
    mobile_number = Column(String)
    email_address = Column(String)

    __table_args__ = (
        UniqueConstraint('patient_id', 'data_source_id'),
    )


class EthnicityCode(StringLookupTable):
    __tablename__ = 'ethnicity_codes'


class PatientAlias(db.Model, MetaModelMixin):
    __tablename__ = 'patient_aliases'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    first_name = Column(String)
    last_name = Column(String)


class PatientAddress(db.Model, MetaModelMixin):
    __tablename__ = 'patient_addresses'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

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


class PatientNumber(db.Model, MetaModelMixin):
    __tablename__ = 'patient_numbers'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    organisation_id = Column(Integer, ForeignKey('organisations.id'), nullable=False)
    organisation = relationship('Organisation')

    number = Column(String, nullable=False)

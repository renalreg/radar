from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, select, DateTime, Boolean, join, Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, aliased

from radar.lib.database import db
from radar.lib.models import MetaModelMixin
from radar.lib.models.patient_demographics import PatientDemographics


class Patient(db.Model, MetaModelMixin):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)

    # TODO move
    # recruited_user_id = Column(Integer, ForeignKey('users.id'))
    # recruited_user = relationship('User')
    # recruited_date = Column(DateTime(timezone=False), default=datetime.now)
    # recruited_organisation_id = Column(Integer, ForeignKey('organisations.id'))
    # recruited_organisation = relationship('Organisation')

    is_active = Column(Boolean, nullable=False, default=True, server_default='1')
    comments = Column(Text)

    organisation_patients = relationship('OrganisationPatient')
    cohort_patients = relationship('CohortPatient')

    patient_demographics = relationship('PatientDemographics')
    patient_numbers = relationship('PatientNumber')
    patient_aliases = relationship('PatientAlias')

    @property
    def organisations(self):
        return [x.organisation for x in self.organisation_patients]

    @property
    def cohorts(self):
        return [x.cohort for x in self.cohort_patients]

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
    def date_of_death(self):
        return self.latest_demographics_attr('date_of_death')

    # TODO test this
    @hybrid_property
    def ethnicity_code(self):
        return self.latest_demographics_attr('ethnicity_code')

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

    @date_of_death.expression
    def date_of_death(cls):
        return cls.latest_demographics_query(PatientDemographics.date_of_death)

    # TODO test this
    @date_of_birth.expression
    def ethnicity_code(cls):
        return cls.latest_demographics_query(PatientDemographics.ethnicity_code)

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

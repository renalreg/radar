from collections import OrderedDict
from sqlalchemy import Column, Integer, ForeignKey, String, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from radar.lib.database import db
from radar.lib.models.common import MetaModelMixin, StringLookupTable

GENDER_MALE = 'M'
GENDER_FEMALE = 'F'

GENDERS = OrderedDict([
    (GENDER_MALE, 'Male'),
    (GENDER_FEMALE, 'Female'),
])


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

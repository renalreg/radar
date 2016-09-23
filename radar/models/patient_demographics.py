from sqlalchemy import Column, Integer, ForeignKey, String, Date, Index
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship
from radar.models.logs import log_changes
from radar.models.patients import GENDERS, ETHNICITIES


@log_changes
class PatientDemographics(db.Model, MetaModelMixin):
    __tablename__ = 'patient_demographics'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('patient_demographics')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_type = Column(String, nullable=False)

    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    date_of_death = Column(Date)
    gender = Column(Integer)
    ethnicity = Column(String)
    home_number = Column(String)
    work_number = Column(String)
    mobile_number = Column(String)
    email_address = Column(String)

    @property
    def year_of_birth(self):
        date_of_birth = self.date_of_birth

        if date_of_birth is None:
            year_of_birth = None
        else:
            year_of_birth = date_of_birth.year

        return year_of_birth

    @property
    def year_of_death(self):
        date_of_death = self.date_of_death

        if date_of_death is None:
            year_of_death = None
        else:
            year_of_death = date_of_death.year

        return year_of_death

    @property
    def gender_label(self):
        return GENDERS.get(self.gender)

    @property
    def ethnicity_label(self):
        return ETHNICITIES.get(self.ethnicity)


Index('patient_demographics_patient_idx', PatientDemographics.patient_id)
Index(
    'patient_demographics_patient_source_idx',
    PatientDemographics.patient_id,
    PatientDemographics.source_group_id,
    PatientDemographics.source_type,
    unique=True
)

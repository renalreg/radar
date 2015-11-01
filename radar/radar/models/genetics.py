from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, Boolean, Index
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, UUIDPKColumn


class Genetics(db.Model, MetaModelMixin):
    __tablename__ = 'genetics'

    id = UUIDPKColumn()

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    cohort_id = Column(Integer, ForeignKey('cohorts.id'), nullable=False)
    cohort = relationship('Cohort')

    sample_sent = Column(Boolean, nullable=False)
    sample_sent_date = Column(DateTime(timezone=True))
    laboratory = Column(String)
    laboratory_reference_number = Column(String)
    results = Column(Text)

Index('genetics_patient_id_idx', Genetics.patient_id)
Index('genetics_cohort_id_idx', Genetics.cohort_id)

from collections import OrderedDict

from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, Index
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship

GENETICS_KARYOTYPES = OrderedDict([
    (1, 'XX'),
    (2, 'XY'),
    (9, 'Not Done'),
    (8, 'Other'),
])


class Genetics(db.Model, MetaModelMixin):
    __tablename__ = 'genetics'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('genetics')

    cohort_id = Column(Integer, ForeignKey('cohorts.id'), nullable=False)
    cohort = relationship('Cohort')

    date_sent = Column(DateTime(timezone=True))
    laboratory = Column(String)
    reference_number = Column(String)
    karyotype = Column(Integer)
    results = Column(Text)
    summary = Column(Text)

Index('genetics_patient_id_idx', Genetics.patient_id)
Index('genetics_cohort_id_idx', Genetics.cohort_id)

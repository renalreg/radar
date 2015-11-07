from collections import OrderedDict

from sqlalchemy import Column, Integer, ForeignKey, Date, String, Index
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column

DIAGNOSIS_BIOPSY_DIAGNOSES = OrderedDict([
    (1, 'Minimal Change'),
    (2, 'FSGS'),
    (3, 'Mesangial Hyperthrophy'),
    (4, 'Other'),
    (5, 'No BX @ Time of Diagnosis'),
])


class Diagnosis(db.Model, MetaModelMixin):
    __tablename__ = 'diagnoses'

    id = uuid_pk_column()

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    cohort_id = Column(Integer, ForeignKey('cohorts.id'), nullable=False)
    cohort = relationship('Cohort')

    date_of_onset = Column(Date, nullable=False)
    date_of_diagnosis = Column(Date, nullable=False)

    cohort_diagnosis_id = Column(Integer, ForeignKey('cohort_diagnoses.id'), nullable=False)
    cohort_diagnosis = relationship('CohortDiagnosis')

    diagnosis_text = Column(String)
    biopsy_diagnosis = Column(Integer)

Index('diagnoses_patient_id_idx', Diagnosis.patient_id)
Index('diagnoses_cohort_id_idx', Diagnosis.cohort_id)


class CohortDiagnosis(db.Model):
    __tablename__ = 'cohort_diagnoses'

    id = Column(Integer, primary_key=True)

    cohort_id = Column(Integer, ForeignKey('cohorts.id'), nullable=False)
    cohort = relationship('Cohort')

    label = Column(String, nullable=False)

Index('cohort_diagnoses_cohort_id_idx', CohortDiagnosis.cohort_id)

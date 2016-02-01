from sqlalchemy import Column, Date, Index

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship
from radar.models.logs import log_changes


@log_changes
class RenalDiagnosis(db.Model, MetaModelMixin):
    __tablename__ = 'renal_diagnoses'

    id = uuid_pk_column()

    patient_id = patient_id_column(unique=True)
    patient = patient_relationship('renal_diagnoses')

    onset_date = Column(Date)
    esrf_date = Column(Date)

Index('renal_diagnoses_patient_idx', RenalDiagnosis.patient_id)

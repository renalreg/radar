from sqlalchemy import Column, Date, Index

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship
from radar.models.logs import log_changes


@log_changes
class RenalProgression(db.Model, MetaModelMixin):
    __tablename__ = 'renal_progressions'

    id = uuid_pk_column()

    patient_id = patient_id_column(unique=True)
    patient = patient_relationship(__tablename__)

    onset_date = Column(Date)
    ckd3a_date = Column(Date)
    ckd3b_date = Column(Date)
    ckd4_date = Column(Date)
    ckd5_date = Column(Date)
    esrf_date = Column(Date)

Index('renal_progressions_patient_idx', RenalProgression.patient_id)

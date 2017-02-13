from sqlalchemy import Column, Index, Integer

from radar.database import db
from radar.models.common import patient_id_column, patient_relationship


class PatientLock(db.Model):
    __tablename__ = 'patient_locks'

    id = Column(Integer, primary_key=True)

    patient_id = patient_id_column()
    patient = patient_relationship('patient_locks')

    sequence_number = Column(Integer)

Index('patient_locks_patient_idx', PatientLock.patient_id)

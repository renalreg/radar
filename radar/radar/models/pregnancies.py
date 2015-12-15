from sqlalchemy import Column, Integer, Date, Index, Boolean

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship


class Pregnancy(db.Model, MetaModelMixin):
    __tablename__ = 'pregnancies'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('pregnancies')

    sequence_number = Column(Integer, nullable=False)
    date_of_lmp = Column(Date, nullable=False)
    gravidity = Column(Integer)
    parity1 = Column(Integer)
    parity2 = Column(Integer)
    outcome = Column(Integer)
    weight = Column(Integer)
    weight_centile = Column(Integer)
    gestational_age = Column(Integer)
    delivery_method = Column(Integer)
    neonatal_intensive_care = Column(Boolean)
    pre_eclampsia = Column(Integer)

Index('pregnancies_patient_id', Pregnancy.patient_id)

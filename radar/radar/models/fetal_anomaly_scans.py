from sqlalchemy import Column, Integer, Date, Index, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship


class FetalAnomalyScan(db.Model, MetaModelMixin):
    __tablename__ = 'fetal_anomaly_scans'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('fetal_anomaly_scans')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    date_of_scan = Column(Date, nullable=False)
    gestation_days = Column(Integer, nullable=False)
    oligohydramnios = Column(Boolean)
    right_anomaly_details = Column(String)
    right_ultrasound_details = Column(String)
    left_anomaly_details = Column(String)
    left_ultrasound_details = Column(String)

Index('fetal_anomaly_scans_patient_id_idx', FetalAnomalyScan.patient_id)

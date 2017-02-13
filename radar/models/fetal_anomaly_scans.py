from sqlalchemy import Boolean, Column, Date, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship, uuid_pk_column
from radar.models.logs import log_changes


@log_changes
class FetalAnomalyScan(db.Model, MetaModelMixin):
    __tablename__ = 'fetal_anomaly_scans'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('fetal_anomaly_scans')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_type = Column(String, nullable=False)

    date_of_scan = Column(Date, nullable=False)
    gestational_age = Column(Integer, nullable=False)
    oligohydramnios = Column(Boolean)
    right_anomaly_details = Column(String)
    right_ultrasound_details = Column(String)
    left_anomaly_details = Column(String)
    left_ultrasound_details = Column(String)
    hypoplasia = Column(Boolean)
    echogenicity = Column(Boolean)
    hepatic_abnormalities = Column(Boolean)
    hepatic_abnormality_details = Column(String)
    lung_abnormalities = Column(Boolean)
    lung_abnormality_details = Column(String)
    amnioinfusion = Column(Boolean)
    amnioinfusion_count = Column(Integer)

Index('fetal_anomaly_scans_patient_idx', FetalAnomalyScan.patient_id)

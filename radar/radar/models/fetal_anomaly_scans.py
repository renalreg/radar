from sqlalchemy import Column, Integer, Date, Index, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship


class FetalAnomalyScan(db.Model, MetaModelMixin):
    __tablename__ = 'fetal_anomaly_scans'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('fetal_anomaly_scans')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_type_id = Column(String, ForeignKey('source_types.id'), nullable=False)
    source_type = relationship('SourceType')

    date_of_scan = Column(Date, nullable=False)
    gestational_age = Column(Integer, nullable=False)
    oligohydramnios = Column(Boolean)
    right_anomaly_details = Column(String)
    right_ultrasound_details = Column(String)
    left_anomaly_details = Column(String)
    left_ultrasound_details = Column(String)

Index('fetal_anomaly_scans_patient_idx', FetalAnomalyScan.patient_id)

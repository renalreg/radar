from collections import OrderedDict

from sqlalchemy import Column, Integer, Date, Index, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship

LIQUOR_VOLUMES = OrderedDict([
    ('NORMAL', 'Normal'),
    ('DECREASED', 'Decreased'),
    ('INCREASED', 'Increased'),
])


class FetalUltrasound(db.Model, MetaModelMixin):
    __tablename__ = 'fetal_ultrasounds'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('fetal_ultrasounds')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    date_of_scan = Column(Date, nullable=False)
    fetal_identifier = Column(String)
    gestational_age = Column(Integer)
    head_centile = Column(Integer)
    abdomen_centile = Column(Integer)
    uterine_artery_notched = Column(Boolean)
    liquor_volume = Column(String)
    comments = Column(String)

Index('fetal_ultrasounds_patient_id_idx', FetalUltrasound.patient_id)

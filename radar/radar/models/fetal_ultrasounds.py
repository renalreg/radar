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

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_type_id = Column(String, ForeignKey('source_types.id'), nullable=False)
    source_type = relationship('SourceType')

    date_of_scan = Column(Date, nullable=False)
    fetal_identifier = Column(String)
    gestational_age = Column(Integer)
    head_centile = Column(Integer)
    abdomen_centile = Column(Integer)
    uterine_artery_notched = Column(Boolean)
    liquor_volume = Column(String)
    comments = Column(String)

Index('fetal_ultrasounds_patient_idx', FetalUltrasound.patient_id)

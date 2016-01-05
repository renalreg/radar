from collections import OrderedDict
from sqlalchemy import Column, Integer, ForeignKey, Date, String, Index
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship

PATHOLOGY_KIDNEY_TYPES = OrderedDict([
    ('TRANSPLANT', 'Transplant'),
    ('NATIVE', 'Native'),
])

PATHOLOGY_KIDNEY_SIDES = OrderedDict([
    ('RIGHT', 'Right'),
    ('LEFT', 'Left'),
])


class Pathology(db.Model, MetaModelMixin):
    __tablename__ = 'pathology'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('pathology')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    date = Column(Date, nullable=False)
    kidney_type = Column(String)
    kidney_side = Column(String)
    laboratory_reference_number = Column(String)
    histological_summary = Column(String)

Index('pathology_patient_id_idx', Pathology.patient_id)

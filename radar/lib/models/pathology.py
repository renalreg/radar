from collections import OrderedDict
from sqlalchemy import Column, Integer, ForeignKey, Date, String, Index
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.lib.models.common import MetaModelMixin

PATHOLOGY_KIDNEY_TYPES = OrderedDict([
    ('TRANSPLANT', 'Transplant'),
    ('NATURAL', 'Natural'),
])

PATHOLOGY_KIDNEY_SIDES = OrderedDict([
    ('RIGHT', 'Right'),
    ('LEFT', 'Left'),
])


class Pathology(db.Model, MetaModelMixin):
    __tablename__ = 'pathology'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    date = Column(Date, nullable=False)
    kidney_type = Column(String, nullable=False)
    kidney_side = Column(String, nullable=False)
    laboratory_reference_number = Column(String, nullable=False)
    histological_summary = Column(String)

Index('pathology_patient_id_idx', Pathology.patient_id)

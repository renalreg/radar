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

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_type_id = Column(String, ForeignKey('source_types.id'), nullable=False)
    source_type = relationship('SourceType')

    date = Column(Date, nullable=False)
    kidney_type = Column(String)
    kidney_side = Column(String)
    reference_number = Column(String)
    image_url = Column(String)
    histological_summary = Column(String)
    em_findings = Column(String)

Index('pathology_patient_idx', Pathology.patient_id)

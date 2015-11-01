from collections import OrderedDict
from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, Boolean, DateTime, Index
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, UUIDPKColumn

RENAL_IMAGING_TYPES = OrderedDict([
    ('USS', 'USS'),
    ('CT', 'CT'),
    ('MRI', 'MRI'),
])

RENAL_IMAGING_KIDNEY_TYPES = OrderedDict([
    ('TRANSPLANT', 'Transplant'),
    ('NATURAL', 'Natural'),
])


class RenalImaging(db.Model, MetaModelMixin):
    __tablename__ = 'renal_imaging'

    id = UUIDPKColumn()

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    date = Column(DateTime(timezone=True))

    imaging_type = Column(String)

    right_present = Column(Boolean)
    right_type = Column(String)
    right_length = Column(Numeric)
    right_volume = Column(Numeric)
    right_cysts = Column(Boolean)
    right_calcification = Column(Boolean)
    right_nephrocalcinosis = Column(Boolean)
    right_nephrolithiasis = Column(Boolean)
    right_other_malformation = Column(String)

    left_present = Column(Boolean)
    left_type = Column(String)
    left_length = Column(Numeric)
    left_volume = Column(Numeric)
    left_cysts = Column(Boolean)
    left_calcification = Column(Boolean)
    left_nephrocalcinosis = Column(Boolean)
    left_nephrolithiasis = Column(Boolean)
    left_other_malformation = Column(String)

Index('renal_imaging_patient_id_idx', RenalImaging.patient_id)

from collections import OrderedDict

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, Numeric, String
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship, uuid_pk_column
from radar.models.logs import log_changes


RENAL_IMAGING_TYPES = OrderedDict([
    ('USS', 'USS'),
    ('CT', 'CT'),
    ('MRI', 'MRI'),
])

RENAL_IMAGING_KIDNEY_TYPES = OrderedDict([
    ('TRANSPLANT', 'Transplant'),
    ('NATIVE', 'Native'),
])


@log_changes
class RenalImaging(db.Model, MetaModelMixin):
    __tablename__ = 'renal_imaging'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('renal_imaging')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_type = Column(String, nullable=False)

    date = Column(DateTime(timezone=True))

    imaging_type = Column(String)

    right_present = Column(Boolean)
    right_type = Column(String)
    right_length = Column(Numeric)
    right_volume = Column(Numeric)
    right_cysts = Column(Boolean)
    right_stones = Column(Boolean)
    right_calcification = Column(Boolean)
    right_nephrocalcinosis = Column(Boolean)
    right_nephrolithiasis = Column(Boolean)
    right_other_malformation = Column(String)

    left_present = Column(Boolean)
    left_type = Column(String)
    left_length = Column(Numeric)
    left_volume = Column(Numeric)
    left_cysts = Column(Boolean)
    left_stones = Column(Boolean)
    left_calcification = Column(Boolean)
    left_nephrocalcinosis = Column(Boolean)
    left_nephrolithiasis = Column(Boolean)
    left_other_malformation = Column(String)


Index('renal_imaging_patient_idx', RenalImaging.patient_id)

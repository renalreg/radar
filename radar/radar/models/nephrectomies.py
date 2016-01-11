from collections import OrderedDict

from sqlalchemy import Column, Integer, ForeignKey, Date, Index, String
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship

NEPHRECTOMY_KIDNEY_SIDES = OrderedDict([
    ('LEFT', 'Left'),
    ('RIGHT', 'Right'),
    ('BILATERAL', 'Bilateral'),
])

NEPHRECTOMY_KIDNEY_TYPES = OrderedDict([
    ('TRANSPLANT', 'Transplant'),
    ('NATIVE', 'Native'),
])

NEPHRECTOMY_ENTRY_TYPES = OrderedDict([
    ('O', 'Open'),
    ('HA', 'Hand Assisted'),
    ('TPL', 'Transperitoneal Laparoscopic'),
    ('RPL', 'Retroperitoneal Laparoscopic'),
])


class Nephrectomy(db.Model, MetaModelMixin):
    __tablename__ = 'nephrectomies'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('nephrectomies')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_type_id = Column(String, ForeignKey('source_types.id'), nullable=False)
    source_type = relationship('SourceType')

    date = Column(Date, nullable=False)
    kidney_side = Column(String, nullable=False)
    kidney_type = Column(String, nullable=False)
    entry_type = Column(String, nullable=False)

Index('nephrectomies_patient_idx', Nephrectomy.patient_id)

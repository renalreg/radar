from collections import OrderedDict

from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, Index
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship

GENETICS_KARYOTYPES = OrderedDict([
    (1, 'XX'),
    (2, 'XY'),
    (9, 'Not Done'),
    (8, 'Other'),
])


class Genetics(db.Model, MetaModelMixin):
    __tablename__ = 'genetics'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('genetics')

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship('Group')

    date_sent = Column(DateTime(timezone=True), nullable=False)
    laboratory = Column(String)
    reference_number = Column(String)
    karyotype = Column(Integer)
    results = Column(Text)
    summary = Column(Text)

Index('genetics_patient_idx', Genetics.patient_id)
Index('genetics_group_idx', Genetics.group_id)

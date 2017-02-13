from collections import OrderedDict

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship, uuid_pk_column
from radar.models.logs import log_changes


GENETICS_KARYOTYPES = OrderedDict([
    (1, 'XX'),
    (2, 'XY'),
    (9, 'Not Done'),
    (8, 'Other'),
])


@log_changes
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

    @property
    def karyotype_label(self):
        return GENETICS_KARYOTYPES.get(self.karyotype)

Index('genetics_patient_idx', Genetics.patient_id)
Index('genetics_group_idx', Genetics.group_id)

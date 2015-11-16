from collections import OrderedDict
from sqlalchemy import Column, Integer, ForeignKey, Date, String, Index

from sqlalchemy.orm import relationship
from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship

TRANSPLANT_TYPES = OrderedDict([
    ('DBD', 'DBD'),
    ('DCD', 'DCD'),
    ('LIVE', 'Live'),
])


class Transplant(db.Model, MetaModelMixin):
    __tablename__ = 'transplants'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('transplants')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    transplant_date = Column(Date, nullable=False)
    transplant_type = Column(String, nullable=False)
    date_failed = Column(Date)

    # TODO
    # recurrence = Column(Boolean)
    # date_recurred = Column(Date)

Index('transplants_patient_id_idx', Transplant.patient_id)

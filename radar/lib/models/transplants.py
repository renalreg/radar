from collections import OrderedDict
from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean, String, Index
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.lib.models.common import MetaModelMixin

TRANSPLANT_TYPES = OrderedDict([
    ('DBD', 'DBD'),
    ('DCD', 'DCD'),
    ('LIVE', 'Live'),
])


class Transplant(db.Model, MetaModelMixin):
    __tablename__ = 'transplants'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    transplant_date = Column(Date, nullable=False)
    transplant_type = Column(String, nullable=False)
    date_failed = Column(Date)

    # TODO
    # recurrence = Column(Boolean)
    # date_recurred = Column(Date)

Index('transplants_patient_id_idx', Transplant.patient_id)

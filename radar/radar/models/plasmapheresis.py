from collections import OrderedDict
from sqlalchemy import Column, Integer, ForeignKey, String, Index
from sqlalchemy import Date
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship

PLASMAPHERESIS_RESPONSES = OrderedDict([
    ('COMPLETE', 'Complete'),
    ('PARTIAL', 'Partial'),
    ('NONE', 'None'),
])

PLASMAPHERESIS_NO_OF_EXCHANGES = OrderedDict([
    ('1/1D', 'Daily'),
    ('5/1W', 'x5 / week'),
    ('4/1W', 'x4 / week'),
    ('3/1W', 'x3 / week'),
    ('2/1W', 'x2 / week'),
    ('1/1W', 'x1 / week'),
    ('1/2W', 'x1 / 2 weeks'),
    ('1/4W', 'x1 / 4 weeks'),
])


class Plasmapheresis(db.Model, MetaModelMixin):
    __tablename__ = 'plasmapheresis'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('plasmapheresis')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_id = Column(String, ForeignKey('sources.id'), nullable=False)
    source = relationship('Source')

    from_date = Column(Date, nullable=False)
    to_date = Column(Date)
    no_of_exchanges = Column(String)
    response = Column(String)

Index('plasmapheresis_patient_id_idx', Plasmapheresis.patient_id)

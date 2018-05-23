from collections import OrderedDict

from sqlalchemy import Column, ForeignKey, Index, Integer, String
from sqlalchemy import Date
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship, uuid_pk_column
from radar.models.logs import log_changes


PLASMAPHERESIS_RESPONSES = OrderedDict([
    ('COMPLETE', 'Complete'),
    ('PARTIAL', 'Partial'),
    ('PREEMTIVE', 'Preemptive'),
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


@log_changes
class Plasmapheresis(db.Model, MetaModelMixin):
    __tablename__ = 'plasmapheresis'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('plasmapheresis')

    source_group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    source_group = relationship('Group')
    source_type = Column(String, nullable=False)

    from_date = Column(Date, nullable=False)
    to_date = Column(Date)
    no_of_exchanges = Column(String)
    response = Column(String)

    @property
    def no_of_exchanges_label(self):
        return PLASMAPHERESIS_NO_OF_EXCHANGES.get(self.no_of_exchanges)

    @property
    def response_label(self):
        return PLASMAPHERESIS_RESPONSES.get(self.response)


Index('plasmapheresis_patient_idx', Plasmapheresis.patient_id)

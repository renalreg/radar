from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy import Date
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.lib.models.common import MetaModelMixin


# TODO
PLASMAPHERESIS_RESPONSES = ['FOO', 'BAR', 'BAZ']


class Plasmapheresis(db.Model, MetaModelMixin):
    __tablename__ = 'plasmapheresis'

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship('Patient')

    data_source_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    data_source = relationship('DataSource')

    from_date = Column(Date, nullable=False)
    to_date = Column(Date)
    no_of_exchanges = Column(Integer)
    response = Column(String)

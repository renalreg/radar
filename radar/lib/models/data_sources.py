from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from radar.lib.database import db

DATA_SOURCE_TYPE_RADAR = 'RADAR'
DATA_SOURCE_TYPE_PV = 'PV'

DATA_SOURCE_TYPES = [
    DATA_SOURCE_TYPE_RADAR,
    DATA_SOURCE_TYPE_PV
]


class DataSource(db.Model):
    __tablename__ = 'data_sources'

    id = Column(Integer, primary_key=True)

    organisation_id = Column(Integer, ForeignKey('organisations.id'), nullable=False)
    organisation = relationship('Organisation')

    type = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('organisation_id', 'type'),
    )

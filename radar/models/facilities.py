from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from radar.lib.database import db


class Facility(db.Model):
    __tablename__ = 'facilities'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String, nullable=False)

    unit_id = Column(Integer, ForeignKey('units.id'))
    unit = relationship('Unit')

    is_internal = Column(Boolean, nullable=False)

    @property
    def is_radar(self):
        return self.code == 'RADAR'

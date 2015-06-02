from sqlalchemy import Column, Integer, String

from radar.lib.database import db


class Facility(db.Model):
    __tablename__ = 'facilities'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)

    @property
    def is_radar(self):
        return self.code == 'RADAR'

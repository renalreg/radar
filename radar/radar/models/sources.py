from sqlalchemy import String, Column

from radar.database import db

SOURCE_RADAR = 'RADAR'
SOURCE_UKRDC = 'UKRDC'


class Source(db.Model):
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)

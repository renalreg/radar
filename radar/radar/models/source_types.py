from sqlalchemy import String, Column

from radar.database import db

SOURCE_TYPE_RADAR = 'RADAR'
SOURCE_TYPE_UKRDC = 'UKRDC'


class SourceType(db.Model):
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)

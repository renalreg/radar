from sqlalchemy import Column, ForeignKey, Integer, String

from radar.database import db


class Nationality(db.Model):
    __tablename__ = 'nationalities'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    test = Column(String)


class GroupNationality(db.Model):
    __tablename__ = 'group_nationalities'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'))
    nationality_id = Column(Integer, ForeignKey('nationalities.id'))

from sqlalchemy import Column, ForeignKey, Integer, String

from radar.database import db


class Ethnicity(db.Model):
    __tablename__ = 'ethnicities'

    id = Column(Integer, primary_key=True)
    code = Column(String(length=50), nullable=False)
    label = Column(String(length=100), nullable=False)


class GroupEthnicity(db.Model):
    __tablename__ = 'group_ethnicities'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'))
    ethnicity_id = Column(Integer, ForeignKey('ethnicities.id'))


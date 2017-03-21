from sqlalchemy import Column, String

from radar.database import db


class Country(db.Model):
    __tablename__ = 'countries'

    code = Column(String(length=2), primary_key=True)
    label = Column(String(length=100), nullable=False)

    def __str__(self):
        return self.label

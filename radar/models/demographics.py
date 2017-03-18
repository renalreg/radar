from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship
from radar.database import db


class Ethnicity(db.Model):
    __tablename__ = 'ethnicities'

    id = Column(Integer, primary_key=True)
    code = Column(String(length=10))
    label = Column(String)


class CountryEthnicity(db.Model):
    __tablename__ = 'country_ethnicities'

    id = Column(Integer, primary_key=True)

    ethnicity_id = Column(Integer, ForeignKey('ethnicities.id'))
    ethnicity = relationship('Ethnicity', foreign_keys=[ethnicity_id], backref=backref('countries', lazy='joined'))

    country_code = Column(String(length=2), ForeignKey('countries.code'))
    country = relationship('Country', foreign_keys=[country_code], backref=backref('ethnicities'))


class Nationality(db.Model):
    __tablename__ = 'nationalities'

    id = Column(Integer, primary_key=True)
    label = Column(String)


class CountryNationality(db.Model):
    __tablename__ = 'country_nationalities'

    id = Column(Integer, primary_key=True)

    nationality_id = Column(Integer, ForeignKey('nationalities.id'))
    nationality = relationship(
        'Nationality',
        foreign_keys=[nationality_id],
        backref=backref('countries', lazy='joined')
    )

    country_code = Column(String(length=2), ForeignKey('countries.code'))
    country = relationship('Country', foreign_keys=[country_code], backref=backref('nationalities'))

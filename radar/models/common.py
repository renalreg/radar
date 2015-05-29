from sqlalchemy import Integer, Column, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from radar.lib.database import db


class CreatedMixin(object):
    @declared_attr
    def created_user_id(cls):
        return Column(Integer, ForeignKey('users.id'))

    @declared_attr
    def created_user(cls):
        return relationship('User', foreign_keys=[cls.created_user_id])

    @declared_attr
    def created_date(cls):
        return Column(DateTime(timezone=True), server_default=func.now())


class ModifiedMixin(object):
    @declared_attr
    def modified_user_id(cls):
        return Column(Integer, ForeignKey('users.id'))

    @declared_attr
    def modified_user(cls):
        return relationship('User', foreign_keys=[cls.modified_user_id])

    @declared_attr
    def modified_date(cls):
        return Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())


class MetadataMixin(CreatedMixin, ModifiedMixin):
    pass


class IntegerLookupTable(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)

    @classmethod
    def choices(cls, session):
        return [(x.id, x.label, x) for x in session.query(cls).order_by(cls.label).all()]


class StringLookupTable(db.Model):
    __abstract__ = True

    id = Column(String, primary_key=True)
    label = Column(String, nullable=False)

    @classmethod
    def choices(cls, session):
        return [(x.id, x.name, x) for x in session.query(cls).order_by(cls.label).all()]
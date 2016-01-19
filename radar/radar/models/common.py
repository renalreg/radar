from datetime import datetime

from sqlalchemy import Integer, Column, ForeignKey, DateTime, text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects import postgresql


def uuid_pk_column():
    return Column(postgresql.UUID, primary_key=True, server_default=text('uuid_generate_v4()'))


def patient_id_column():
    return Column(Integer, ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)


def patient_relationship(name):
    return relationship('Patient', backref=backref(name, cascade='all, delete-orphan', passive_deletes=True))


class CreatedUserMixin(object):
    @declared_attr
    def created_user_id(cls):
        return Column(Integer, ForeignKey('users.id'), nullable=False)

    @declared_attr
    def created_user(cls):
        return relationship('User', primaryjoin="User.id == %s.created_user_id" % cls.__name__)


class CreatedDateMixin(object):
    @declared_attr
    def created_date(cls):
        return Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, server_default=text('now()'))


class ModifiedUserMixin(object):
    @declared_attr
    def modified_user_id(cls):
        return Column(Integer, ForeignKey('users.id'), nullable=False)

    @declared_attr
    def modified_user(cls):
        return relationship('User', primaryjoin="User.id == %s.modified_user_id" % cls.__name__)


class ModifiedDateMixin(object):
    @declared_attr
    def modified_date(cls):
        return Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, server_default=text('now()'))


class CreatedMixin(CreatedUserMixin, CreatedDateMixin):
    pass


class ModifiedMixin(ModifiedUserMixin, ModifiedDateMixin):
    pass


class MetaModelMixin(CreatedMixin, ModifiedMixin):
    pass

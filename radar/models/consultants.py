from sqlalchemy import Integer, Column, String, ForeignKey, Index
from sqlalchemy.orm import relationship, backref

from radar.database import db
from radar.models.common import MetaModelMixin
from radar.models.logs import log_changes


@log_changes
class Consultant(db.Model, MetaModelMixin):
    __tablename__ = 'consultants'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String)
    telephone_number = Column(String)
    gmc_number = Column(Integer, unique=True)

    specialty_id = Column(Integer, ForeignKey('specialties.id'), nullable=False)
    specialty = relationship('Specialty')

    @property
    def groups(self):
        return [x.group for x in self.group_consultants]


@log_changes
class GroupConsultant(db.Model, MetaModelMixin):
    __tablename__ = 'group_consultants'

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship('Group')

    consultant_id = Column(Integer, ForeignKey('consultants.id'), nullable=False)
    consultant = relationship('Consultant', backref=backref('group_consultants', cascade='all, delete-orphan', passive_deletes=True))

Index(
    'group_consultants_group_consultant_idx',
    GroupConsultant.group_id,
    GroupConsultant.consultant_id,
    unique=True
)


@log_changes
class Specialty(db.Model):
    __tablename__ = 'specialties'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

from sqlalchemy import Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import backref, relationship

from radar.database import db
from radar.models.logs import log_changes


@log_changes
class Consultant(db.Model):
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

    def __unicode__(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)

    __str__ = __unicode__


@log_changes
class GroupConsultant(db.Model):
    __tablename__ = 'group_consultants'

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship('Group')

    consultant_id = Column(
        Integer,
        ForeignKey('consultants.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False)
    consultant = relationship(
        'Consultant',
        backref=backref('group_consultants', cascade='all, delete-orphan', passive_deletes=True))


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

    def __unicode__(self):
        return self.name

    __str__ = __unicode__

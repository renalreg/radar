from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.logs import log_changes


@log_changes
class GroupAntibody(db.Model):
    __tablename__ = 'group_antibodies'

    group_id = Column(
        Integer,
        ForeignKey('groups.id', ondelete='CASCADE'),
        primary_key=True,
    )

    antibody_id = Column(
        String,
        ForeignKey('antibodies.id', ondelete='CASCADE'),
        primary_key=True,
    )

    group = relationship(
        'Group',
        back_populates='group_antibodies',
        passive_deletes=True,
    )

    antibody = relationship(
        'Antibody',
        back_populates='group_antibodies',
        passive_deletes=True,
    )


@log_changes
class Antibody(db.Model):
    __tablename__ = 'antibodies'

    id = Column(String, primary_key=True, nullable=False)
    is_official = Column(Boolean, nullable=False, default=False)

    group_antibodies = relationship(
        'GroupAntibody',
        back_populates='antibody',
        cascade='all, delete-orphan'
    )


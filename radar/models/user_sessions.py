from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import backref, relationship

from radar.database import db
from radar.models.logs import log_changes
from radar.models.users import AnonymousUser


@log_changes
class UserSession(db.Model):
    __tablename__ = 'user_sessions'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    user = relationship('User', backref=backref('user_sessions', cascade='all, delete-orphan', passive_deletes=True))

    date = Column(DateTime(timezone=True), nullable=False)
    ip_address = Column(postgresql.INET, nullable=False)
    user_agent = Column(String, nullable=True)

    @classmethod
    def is_authenticated(cls):
        return True


Index('user_sessions_user_idx', UserSession.user_id)


class AnonymousSession(object):
    """Used when the user isn't logged in."""

    user = AnonymousUser()

    @classmethod
    def is_authenticated(cls):
        return False

from sqlalchemy import String, Column, Integer, ForeignKey, DateTime, Boolean, Index
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.users import User, AnonymousUser
from radar.models.logs import log_changes


@log_changes
class UserSession(db.Model):
    __tablename__ = 'user_sessions'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship(User)

    date = Column(DateTime(timezone=True), nullable=False)
    ip_address = Column(postgresql.INET, nullable=False)
    user_agent = Column(String, nullable=True)

    @classmethod
    def is_authenticated(cls):
        return True

Index('user_sessions_user_idx', UserSession.user_id)


class AnonymousSession(object):
    user = AnonymousUser()

    @classmethod
    def is_authenticated(cls):
        return False

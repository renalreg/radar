from sqlalchemy import String, Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from radar.lib.database import db
from radar.lib.models import User, AnonymousUser


class UserSession(db.Model):
    __tablename__ = 'user_sessions'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship(User)

    date = Column(DateTime(timezone=True), nullable=False)
    ip_address = Column(postgresql.INET, nullable=False)
    user_agent = Column(String, nullable=True)

    is_active = Column(Boolean, nullable=False)

    @classmethod
    def is_authenticated(cls):
        return True


class AnonymousSession(object):
    user = AnonymousUser()

    @classmethod
    def is_authenticated(cls):
        return False

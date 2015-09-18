from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from radar.lib.database import db
from radar.lib.models import User


class UserSession(db.Model):
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship(User)

    token = Column(String)
    user_agent = Column(String)
    ip_address = Column(postgresql.INET)

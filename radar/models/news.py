from sqlalchemy import Column, Integer, Text, DateTime
from radar.database import db


class Story(db.Model):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    published = Column(DateTime(timezone=True), nullable=False)

    def can_edit(self, user):
        return user.is_admin
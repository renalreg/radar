from sqlalchemy import Column, Integer, Text, DateTime

from radar.lib.database import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    published = Column(DateTime(timezone=True), nullable=False)

    def can_view(self, user):
        return True

    def can_edit(self, user):
        return user.is_admin

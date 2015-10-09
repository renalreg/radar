from sqlalchemy import Column, Integer, Text, DateTime

from radar.database import db
from radar.models import MetaModelMixin


class Post(db.Model, MetaModelMixin):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    published_date = Column(DateTime(timezone=True), nullable=False)

from sqlalchemy import Column, Integer, Text, DateTime

from radar.database import db
from radar.models.common import MetaModelMixin
from radar.models.logs import log_changes


@log_changes
class Post(db.Model, MetaModelMixin):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    published_date = Column(DateTime(timezone=True), nullable=False)
    body = Column(Text, nullable=False)

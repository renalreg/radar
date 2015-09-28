from sqlalchemy import Integer, Column, String
from radar.lib.database import db


class Consultant(db.Model):
    __tablename__ = 'consultants'

    id = Column(Integer, primary_key=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship
from radar.lib.database import db


class Consultant(db.Model):
    __tablename__ = 'consultants'

    id = Column(Integer, primary_key=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    organisation_consultants = relationship('OrganisationConsultant')

    @property
    def organisations(self):
        return [x.organisation for x in self.organisation_consultants]

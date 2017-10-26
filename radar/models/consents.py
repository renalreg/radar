from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, text
from sqlalchemy.orm import backref, relationship

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship


class Consent(db.Model):
    __tablename__ = 'consents'

    id = Column(Integer, primary_key=True)
    code = Column(String(length=50), nullable=False)
    label = Column(String)
    paediatric = Column(Boolean, default=False, server_default=text('false'))
    from_date = Column(Date, nullable=False)
    link_url = Column(String, nullable=True)
    retired = Column(Boolean, default=False, server_default=text('false'))

    def __str__(self):
        return self.label


class PatientConsent(db.Model, MetaModelMixin):
    __tablename__ = 'patient_consents'

    id = Column(Integer, primary_key=True)

    consent_id = Column(Integer, ForeignKey('consents.id'))
    consent = relationship('Consent', foreign_keys=[consent_id], backref=backref('consents', lazy='joined'))

    patient_id = patient_id_column()
    patient = patient_relationship('consents')

    signed_on_date = Column(Date, nullable=False)
    withdrawn_on_date = Column(Date, nullable=True)

from sqlalchemy import select, and_, or_, exists, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship, backref

from radar.database import db
from radar.models.medications import Medication
from radar.models.patients import Patient
from radar.models.results import Result
from radar.models.views import create_view


# TODO use ukrdc_importer username rather than hard-coding the ID
class UKRDCPatient(db.Model):
    __table__ = create_view(
        'ukrdc_patients',
        select([Patient.id])
        .where(
            or_(
                exists().where(and_(Result.patient_id == Patient.id, Result.created_user_id == 1658)),
                exists().where(and_(Medication.patient_id == Patient.id, Medication.created_user_id == 1658))
            )
        ),
        PrimaryKeyConstraint('id')
    )

    patient = relationship('Patient',
        primaryjoin='UKRDCPatient.id == Patient.id',
        uselist=False,
        backref='ukrdc_patient',
        foreign_keys='Patient.id'
    )
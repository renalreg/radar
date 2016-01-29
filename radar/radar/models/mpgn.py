from sqlalchemy import Column, Boolean, String, Date, Index

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship
from radar.models.logs import log_changes


@log_changes
class MpgnClinicalPicture(db.Model, MetaModelMixin):
    __tablename__ = 'mpgn_clinical_pictures'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('mpgn_clinical_pictures')

    date_of_picture = Column(Date, nullable=False)
    oedema = Column(Boolean)
    hypertension = Column(Boolean)
    urticaria = Column(Boolean)
    partial_lipodystrophy = Column(Boolean)
    infection = Column(Boolean)
    infection_details = Column(String)
    ophthalmoscopy = Column(Boolean)
    ophthalmoscopy_details = Column(String)
    comments = Column(String)

Index('mpgn_clinical_pictures_patient_idx', MpgnClinicalPicture.patient_id)

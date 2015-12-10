from sqlalchemy import Column, Boolean, String, Index, Date

from radar.database import db
from radar.models.common import MetaModelMixin, uuid_pk_column, patient_id_column, patient_relationship


class InsClinicalPicture(db.Model, MetaModelMixin):
    __tablename__ = 'ins_clinical_pictures'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('ins_clinical_pictures')

    date_of_picture = Column(Date)
    oedema = Column(Boolean)
    hypovalaemia = Column(Boolean)
    fever = Column(Boolean)
    thrombosis = Column(Boolean)
    peritonitis = Column(Boolean)
    pulmonary_odemea = Column(Boolean)
    hypertension = Column(Boolean)
    rash = Column(Boolean)
    rash_details = Column(String)
    possible_immunoisation_trigger = Column(Boolean)
    ophthalmoscopy = Column(Boolean)
    ophthalmoscopy_details = Column(String)
    comments = String()

Index('ins_clinical_pictures_patient_id_idx', InsClinicalPicture.patient_id)

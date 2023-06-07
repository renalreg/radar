from collections import OrderedDict

from sqlalchemy import Column, Date, Index, Integer, String

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship, uuid_pk_column
from radar.models.logs import log_changes


DEAFNESS_NO = 1
DEAFNESS_MINOR = 2
DEAFNESS_HEARING_AID = 3

DEAFNESS_OPTIONS = OrderedDict([
    (DEAFNESS_NO, 'No'),
    (DEAFNESS_MINOR, 'Yes - Minor'),
    (DEAFNESS_HEARING_AID, 'Yes - Hearing Aid Needed'),
])


@log_changes
class AlportClinicalPicture(db.Model, MetaModelMixin):
    __tablename__ = 'alport_clinical_pictures'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('alport_clinical_pictures')

    date_of_picture = Column(Date, nullable=False)
    deafness = Column(Integer, nullable=False)
    deafness_date = Column(Date)
    hearing_aid_date = Column(Date)
    comments = Column(String)


Index('alport_clinical_pictures_patient_idx', AlportClinicalPicture.patient_id)

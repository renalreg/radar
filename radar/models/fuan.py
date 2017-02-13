from collections import OrderedDict

from sqlalchemy import Boolean, Column, Date, Index, Integer, String
from sqlalchemy.dialects import postgresql

from radar.database import db
from radar.models.common import MetaModelMixin, patient_id_column, patient_relationship, uuid_pk_column
from radar.models.logs import log_changes


RELATIVES = OrderedDict([
    (1, 'Mother'),
    (2, 'Father'),
    (3, 'Sister'),
    (4, 'Brother'),
    (5, 'Grandmother - Maternal'),
    (6, 'Grandmother - Paternal'),
    (15, 'Grandfather - Maternal'),
    (16, 'Grandfather - Paternal'),
    (7, 'Aunt - Maternal'),
    (8, 'Aunt - Paternal'),
    (9, 'Uncle - Maternal'),
    (10, 'Uncle - Paternal'),
    (11, 'Cousin - Maternal'),
    (12, 'Cousin - Paternal'),
    (13, 'Half Sister'),
    (14, 'Half Brother'),
    (17, 'Daughter'),
    (18, 'Son'),
])

THP_RESULTS = OrderedDict([
    ('NOT_TESTED', 'Not Tested'),
    ('NORMAL', 'Normal'),
    ('LOW', 'Low - Absent'),
])


@log_changes
class FuanClinicalPicture(db.Model, MetaModelMixin):
    __tablename__ = 'fuan_clinical_pictures'

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship('fuan_clinical_pictures')

    picture_date = Column(Date, nullable=False)
    gout = Column(Boolean)
    gout_date = Column(Date)
    family_gout = Column(Boolean)
    family_gout_relatives = Column(postgresql.ARRAY(Integer))
    thp = Column(String)
    uti = Column(Boolean)
    comments = Column(String)


Index('fuan_clinical_pictures_patient_idx', FuanClinicalPicture.patient_id)

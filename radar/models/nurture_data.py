from sqlalchemy import Column, Integer, text
from sqlalchemy.sql.sqltypes import Boolean

from radar.database import db
from radar.models.common import (
    MetaModelMixin,
    patient_id_column,
    patient_relationship_no_list,
)
from radar.models.logs import log_changes


@log_changes
class NurtureData(db.Model, MetaModelMixin):
    __tablename__ = "nurture_data"

    id = Column(Integer, primary_key=True)
    patient = patient_relationship_no_list("nurture_data")
    patient_id = patient_id_column()
    signed_off_state = Column(Integer, nullable=False)
    blood_tests = Column(
        Boolean, default=True, nullable=False, server_default=text("true")
    )
    interviews = Column(
        Boolean, default=True, nullable=False, server_default=text("true")
    )

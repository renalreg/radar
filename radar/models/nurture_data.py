from sqlalchemy import Column, Integer, text
from sqlalchemy.sql.sqltypes import Boolean
from collections import OrderedDict

from radar.database import db
from radar.models.common import (
    MetaModelMixin,
    patient_id_column,
    patient_relationship_no_list,
)
from radar.models.logs import log_changes

SIGNED_OFF_NOT_COMPLETE = 0
SIGNED_OFF_NURTURE_BASELINE = 1
SIGNED_OFF_FOLLOW_UP = 2
SIGNED_OFF_FOLLOW_UP_REFUSED = 3
SIGNED_OFF_BASELINE_COMPLETE_NO_FUP = 4

SIGNED_OFF = OrderedDict(
    [
        (SIGNED_OFF_NOT_COMPLETE, "Not signed off"),
        (SIGNED_OFF_NURTURE_BASELINE, "Nurture baseline data complete"),
        (SIGNED_OFF_FOLLOW_UP, "Nurture baseline and follow up data complete"),
        (
            SIGNED_OFF_BASELINE_COMPLETE_NO_FUP,
            "Baseline complete, no FUP as Tx or dialysis",
        ),
        (SIGNED_OFF_FOLLOW_UP_REFUSED, "Patient refused Follow Up"),
    ]
)


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

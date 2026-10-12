from typing import TYPE_CHECKING
from collections import OrderedDict

from sqlalchemy import Column, Date, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship

from radar.database import db
from radar.models.common import (
    MetaModelMixin,
    patient_id_column,
    patient_relationship,
    uuid_pk_column,
)
from radar.models.logs import log_changes
from radar.variants import PATHOLOGY_KIDNEY_TYPES, pick

PATHOLOGY_KIDNEY_SIDES = OrderedDict(
    [
        ("RIGHT", "Right"),
        ("LEFT", "Left"),
    ]
)


class MainPathologyColumns:
    """Columns that exist only in the main database."""

    report_cleaned = Column(Date)


class InternationalPathologyColumns:
    """Columns that exist only in the international database (none yet)."""


if TYPE_CHECKING:
    class PATHOLOGY_VARIANT_COLUMNS(
        MainPathologyColumns,
        InternationalPathologyColumns,
    ): ...
else:
    PATHOLOGY_VARIANT_COLUMNS = pick(
        main=MainPathologyColumns,
        international=InternationalPathologyColumns,
    )


@log_changes
class Pathology(PATHOLOGY_VARIANT_COLUMNS, db.Model, MetaModelMixin):
    __tablename__ = "pathology"

    id = uuid_pk_column()

    patient_id = patient_id_column()
    patient = patient_relationship("pathology")

    source_group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    source_group = relationship("Group")
    source_type = Column(String, nullable=False)

    date = Column(Date, nullable=False)
    kidney_type = Column(String)
    kidney_side = Column(String)
    reference_number = Column(String)
    image_url = Column(String)
    histological_summary = Column(String)
    em_findings = Column(String)

    @property
    def kidney_type_label(self):
        return PATHOLOGY_KIDNEY_TYPES.get(self.kidney_type)

    @property
    def kidney_side_label(self):
        return PATHOLOGY_KIDNEY_SIDES.get(self.kidney_side)


Index("pathology_patient_idx", Pathology.patient_id)

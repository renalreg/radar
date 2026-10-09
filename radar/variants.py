from typing import TypeVar, OrderedDict

from radar.config import config
from radar.models import SOURCE_TYPE_UKRDC, SOURCE_TYPE_MANUAL, SOURCE_TYPE_BATCH

T = TypeVar("T")

IS_INTERNATIONAL: bool = bool(config["international"])


def pick(*, international: T, main: T) -> T:
    return international if IS_INTERNATIONAL else main


GROUP_DIAGNOSIS_EXPORT_COLUMNS = pick(
    international=["id", "group", "diagnosis", "weight"],
    main=["id", "group", "type", "diagnosis", "weight"],
)

OBSERVATION_COLUMNS = pick(
    international=[
        "id",
        "name",
        "short_name",
        "value_type",
        "sample_type",
        "pv_code",
        "min_valuemax_value",
        "min_length",
        "max_length",
        "units",
        "options",
    ],
    main=[
        "id",
        "name",
        "short_name",
        "value_type",
        "sample_type",
        "pv_code",
        "min_value",
        "max_value",
        "min_length",
        "max_length",
        "units",
        "options",
    ],
)

SOURCE_TYPE_FIELDS = pick(
    international=[SOURCE_TYPE_MANUAL, SOURCE_TYPE_UKRDC],
    main=[SOURCE_TYPE_MANUAL, SOURCE_TYPE_UKRDC, SOURCE_TYPE_BATCH],
)

SAMPLE_EXPORTER_COLUMNS = pick(
    main=[
        "id",
        "patient_id",
        ("date", "data.date"),
        ("barcode", "data.barcode"),
        ("ins_state", "data.insstate"),
    ],
    international=[
        "id",
        "patient_id",
        "taken_on",
        "barcode",
        "epa",
        "epb",
        "lpa",
        "lpb",
        "uc",
        "ub",
        "ud",
        "fub",
        "sc",
        "sa",
        "sb",
        "rna",
        "wb",
        "protocol_id",
    ],
)

MEDICATION_DOSE_UNITS = pick(
    main=OrderedDict(
        [
            ("g", "g"),
            ("mg", "mg"),
            ("µg", "µg"),
            ("ng", "ng"),
            ("l", "L"),
            ("dl", "dl"),
            ("ml", "ml"),
            ("iu", "IU"),
            ("mmol", "mmol"),
            ("tab", "Tab"),
            ("puff", "Puff"),
            ("unit", "Unit"),
            ("ampoule", "Ampoule"),
            ("drop", "Drop"),
            ("capsule", "Capsule"),
            ("patch", "Patch"),
            ("sachet", "Sachet"),
            ("tbsp", "Table Spoon"),
            ("units", "Units"),
            ("other", "Other"),
        ]
    ),
    international=OrderedDict(
        [
            ("ML", "ml"),
            ("NG", "ng"),
            ("UG", "µg"),
            ("MG", "mg"),
            ("G", "g"),
            ("IU", "IU"),
            ("MMOL", "mmol"),
            ("PUFF", "puff"),
            ("UNIT", "unit"),
        ]
    ),
)


PATHOLOGY_KIDNEY_TYPES = pick(
    main=OrderedDict(
        [
            ("TRANSPLANT", "Transplant"),
            ("NATIVE", "Native"),
            ("TIME ZERO TRANSPLANT", "Time zero transplant"),
        ]
    ),
    international=OrderedDict(
        [
            ("TRANSPLANT", "Transplant"),
            ("NATIVE", "Native"),
        ]
    ),
)


RENAL_IMAGING_TYPES = pick(
    main=OrderedDict(
        [
            ("USS", "USS"),
            ("CT", "CT"),
            ("MRI", "MRI"),
            ("DMSA", "DMSA"),
            ("MAG3", "MAG3"),
        ]
    ),
    international=OrderedDict(
        [
            ("USS", "USS"),
            ("CT", "CT"),
            ("MRI", "MRI"),
        ]
    ),
)


TRANSPLANT_MODALITIES = pick(
    main=OrderedDict(
        [
            (21, "Live - Sibling"),
            (74, "Live - Father"),
            (75, "Live - Mother"),
            (73, "Live - Parent"),
            (77, "Live - Child"),
            (23, "Live - Other Relative"),
            (24, "Live - Gentically Unrelated"),
            (26, "Live - With Transplant of Other Organ"),
            (27, "Live - Non-UK"),
            (78, "Live - Unknown"),
            (20, "Cadaver"),
            (25, "Cadaver - With Transplant of Other Organ"),
            (28, "DCD - Non-Heart-Beating"),
            (29, "Unknown"),
            (300, "DBD - Heart-Beating"),
        ]
    ),
    international=OrderedDict(
        [
            (21, "Live - Sibling"),
            (74, "Live - Father"),
            (75, "Live - Mother"),
            (77, "Live - Child"),
            (23, "Live - Other Relative"),
            (24, "Live - Gentically Unrelated"),
            (26, "Live - With Transplant of Other Organ"),
            (27, "Live - Non-UK"),
            (20, "Cadaver"),
            (25, "Cadaver - With Transplant of Other Organ"),
            (28, "Non-Heart-Beating"),
            (29, "Unknown"),
        ]
    ),
)

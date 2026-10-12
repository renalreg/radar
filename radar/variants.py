import os
from typing import OrderedDict
from typing import TypeVar

T = TypeVar("T")

ENV_VAR = "INTERNATIONAL"
_TRUE = {"1", "true", "yes", "on"}
_FALSE = {"0", "false", "no", "off", ""}


def _read_flag() -> bool:
    """INTERNATIONAL=true -> international. Not set, or false -> main."""
    value = os.environ.get(ENV_VAR, "").strip().lower()

    if value in _TRUE:
        return True
    if value in _FALSE:
        return False

    # Fail loudly on typos rather than silently running as main
    raise RuntimeError(f"{ENV_VAR} must be true or false, got {value!r}")


IS_INTERNATIONAL: bool = _read_flag()


def pick(*, international: T, main: T) -> T:
    return international if IS_INTERNATIONAL else main


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

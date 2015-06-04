from radar.lib.database import db
from radar.models import DialysisType

DIALYSIS_TYPES = [
    'HD',
    'PD',
]


def create_dialysis_types():
    for v in DIALYSIS_TYPES:
        dialysis_type = DialysisType(label=v)
        db.session.add(dialysis_type)

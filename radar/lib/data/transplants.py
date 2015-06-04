from radar.lib.database import db
from radar.models import TransplantType

# TODO
TRANSPLANT_TYPES = [
    'Foo',
    'Bar',
    'Baz',
]

def create_transplant_types():
    for v in TRANSPLANT_TYPES:
        transplant_type = TransplantType(label=v)
        db.session.add(transplant_type)

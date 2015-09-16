from radar.lib.database import db
from radar.lib.models import Disorder

DISORDERS = [
    'Heart Disease',
]


def create_disorders():
    for v in DISORDERS:
        disorder = Disorder(label=v)
        db.session.add(disorder)

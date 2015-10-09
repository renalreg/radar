from radar.data.validation import validate
from radar.database import db
from radar.models import Disorder

DISORDERS = [
    'Heart Disease',
    'Cerebral Palsy',
    'Microcoria',
    'Polydactyly',
    'Epilepsy',
    'Atrial Septal Defect',
    'Congenital CMV'
]


def create_disorders():
    for v in DISORDERS:
        disorder = Disorder(label=v)
        disorder = validate(disorder)
        db.session.add(disorder)

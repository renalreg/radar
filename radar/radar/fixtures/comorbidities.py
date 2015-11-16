from radar.fixtures.validation import validate_and_add
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
        validate_and_add(disorder)

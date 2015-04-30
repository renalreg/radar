from radar.concepts.core import Concept
from radar.sda.models import SDAMedication
from radar.validators import required, not_empty


class MedicationConcept(Concept):
    validators = {
        'from_date': [required],
        'name': [not_empty],
    }

    def __init__(self, from_date, to_date, name):
        super(MedicationConcept, self).__init__()

        self.from_date = from_date
        self.to_date = to_date
        self.name = name

    def validate(self):
        if not super(MedicationConcept, self).validate():
            return False

        if self.to_date is not None and self.to_date < self.from_date:
            self.errors['to_date'].append('Must be on or after from date.')

        print not self.errors

    def to_sda(self, sda_bundle):
        sda_medication = SDAMedication()

        data = dict()

        data['from_time'] = self.from_date

        if self.to_date is not None:
            data['to_time'] = self.to_date

        data['order_item'] = {
            'description': self.name
        }

        sda_medication.data = data

        sda_bundle.sda_medications.append(sda_medication)
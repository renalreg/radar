from radar.concepts.core import Concept
from radar.sda.models import SDAMedication
from radar.validators import required, not_empty


class MedicationConcept(Concept):
    validators = {
        'from_date': [required],
        'name': [not_empty],
        'dose_quantity': [required],
        'dose_unit': [required],
        'frequency': [required],
        'route': [required],
    }

    def __init__(self, from_date, to_date, name, dose_quantity, dose_unit, frequency, route):
        super(MedicationConcept, self).__init__()

        self.from_date = from_date
        self.to_date = to_date
        self.name = name
        self.dose_quantity = dose_quantity
        self.dose_unit = dose_unit
        self.frequency = frequency
        self.route = route

    def validate(self):
        if not super(MedicationConcept, self).validate():
            return False

        if self.to_date is not None and self.to_date < self.from_date:
            self.errors['to_date'].append('Must be on or after from date.')

        return not self.errors

    def to_sda(self, sda_bundle):
        sda_medication = SDAMedication()

        data = {
            'from_time': self.from_date,
            'order_item': {
                'description': self.name
            },
            'dose_quantity': self.dose_quantity,
            'dose_uom': {
                'sda_coding_standard': 'RADAR',
                'code': self.dose_unit.id,
                'description': self.dose_unit.name,
            },
            'frequency': {
                'sda_coding_standard': 'RADAR',
                'code': self.frequency.id,
                'description': self.frequency.name,
            },
            'route': {
                'sda_coding_standard': 'RADAR',
                'code': self.route.id,
                'description': self.route.name,
            },
            'entering_organization': {
                'code': sda_bundle.facility.code,
                'description': sda_bundle.facility.name,
            }
        }

        if self.to_date is not None:
            data['to_time'] = self.to_date

        sda_medication.data = data

        sda_bundle.sda_medications.append(sda_medication)
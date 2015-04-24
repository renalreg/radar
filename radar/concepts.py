from collections import defaultdict

from radar.models import SDAMedication, SDAPatient
from radar.validators import ValidationError, StopValidation, required, not_empty

# TODO refactor

class Concept(object):
    validators = {}

    def __init__(self):
        self._reset()

    def _reset(self):
        self.errors = defaultdict(list)

    def _valid(self):
        return not any(len(x) for x in self.errors)

    def _validate(self):
        self._reset()

        for model_key, validators in self.validators.items():
            model_value = getattr(self, model_key)

            for validator in validators:
                try:
                    validator(model_value)
                except ValidationError as e:
                    self.errors[model_key].append(e.message)
                    break
                except StopValidation:
                    break

        if not self._valid():
            return

        self.validate()

    def validate(self):
        pass

    def valid(self):
        self._validate()
        return self._valid()

    def to_sda(self):
        pass

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
        super(MedicationConcept, self).validate()

        if self.to_date is not None:
            if self.to_date < self.from_date:
                self.errors['to_date'].append('Must be on or after from date.')

    def to_sda(self, sda_resource):
        sda_medication = SDAMedication()

        sda_medication.data = {
            'from_time': self.from_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'order_item': {
                'description': self.name
            }
        }

        if self.to_date is not None:
            sda_medication.data['to_time'] = self.to_date.strftime('%Y-%m-%dT%H:%M:%SZ')

        sda_resource.sda_medications.append(sda_medication)

class PatientConcept(Concept):
    validators = {
        'first_name': [not_empty],
        'last_name': [not_empty],
    }

    def __init__(self, first_name, last_name):
        super(PatientConcept, self).__init__()

        self.first_name = first_name
        self.last_name = last_name

    def to_sda(self, sda_resource):
        sda_patient = SDAPatient()

        sda_patient.data = {
            'name': {
                'given_name': self.first_name,
                'family_name': self.last_name
            }
        }

        sda_resource.sda_patient = sda_patient
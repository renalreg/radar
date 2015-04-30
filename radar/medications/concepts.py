from collections import defaultdict

from radar.concepts.medications import MedicationConcept


class MedicationToMedicationConcept(object):
    def __init__(self, medication):
        self.medication = medication

        self.medication_concept = MedicationConcept(
            self.medication.from_date,
            self.medication.to_date,
            self.medication.name
        )

    def validate(self):
        errors = defaultdict(list)

        if self.medication_concept.validate():
            return True, errors
        else:
            errors['from_date'].extend(self.medication_concept.errors['from_date'])
            errors['to_date'].extend(self.medication_concept.errors['to_date'])
            errors['name'].extend(self.medication_concept.errors['name'])

            return False, errors

    def to_sda(self, sda_bundle):
        self.medication_concept.to_sda(sda_bundle)
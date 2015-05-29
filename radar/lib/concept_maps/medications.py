from collections import defaultdict

from radar.lib.concepts.medications import MedicationConcept


class MedicationConceptMap(object):
    def __init__(self, medication):
        self.medication = medication

        self.medication_concept = MedicationConcept(
            self.medication.from_date,
            self.medication.to_date,
            self.medication.name,
            self.medication.dose_quantity,
            self.medication.dose_unit,
            self.medication.frequency,
            self.medication.route,
        )

    def validate(self):
        valid = True
        errors = defaultdict(list)

        if not self.medication_concept.validate():
            valid = False
            errors['from_date'].extend(self.medication_concept.errors['from_date'])
            errors['to_date'].extend(self.medication_concept.errors['to_date'])
            errors['name'].extend(self.medication_concept.errors['name'])
            errors['dose_quantity'].extend(self.medication_concept.errors['dose_quantity'])
            errors['dose_unit_id'].extend(self.medication_concept.errors['dose_unit'])
            errors['frequency_id'].extend(self.medication_concept.errors['frequency'])
            errors['route_id'].extend(self.medication_concept.errors['route'])

        return valid, errors

    def to_sda(self, sda_bundle):
        self.medication_concept.to_sda(sda_bundle)
from datetime import date
import random

from radar.fixtures.constants import MEDICATION_NAMES
from radar.fixtures.utils import random_date, add
from radar.models.medications import Medication, MEDICATION_DOSE_UNITS, MEDICATION_ROUTES


def create_medications_f():
    def create_medications(patient, source_group, source_type, n):
        for _ in range(n):
            medication = Medication()
            medication.patient = patient
            medication.source_group = source_group
            medication.source_type = source_type
            medication.from_date = random_date(patient.earliest_date_of_birth, date.today())

            if random.random() > 0.5:
                medication.to_date = random_date(medication.from_date, date.today())

            medication.drug_text = random.choice(MEDICATION_NAMES)
            medication.dose_quantity = random.randint(1, 10)
            medication.dose_unit = random.choice(MEDICATION_DOSE_UNITS.keys())
            medication.frequency = 'Daily'
            medication.route = random.choice(MEDICATION_ROUTES.keys())

            add(medication)

    return create_medications

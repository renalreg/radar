from radar.lib.database import db
from radar.models import MedicationRoute, MedicationDoseUnit, MedicationFrequency

# TODO
MEDICATION_ROUTES = [
    ('Oral', 'Oral'),
    ('Rectal', 'Rectal'),
]

# TODO
MEDICATION_DOSE_UNITS = [
    ('ml', 'ml'),
    ('l', 'l'),
    ('mg', 'mg'),
    ('g', 'g'),
    ('kg', 'kg'),
]

# TODO
MEDICATION_FREQUENCIES = [
    ('Daily', 'Daily'),
    ('Weekly', 'Weekly'),
    ('Monthly', 'Monthly'),
]


def create_medication_routes():
    for k, v in MEDICATION_ROUTES:
        medication_route = MedicationRoute(id=k, label=v)
        db.session.add(medication_route)


def create_medication_dose_units():
    for k, v, in MEDICATION_DOSE_UNITS:
        medication_dose_unit = MedicationDoseUnit(id=k, label=v)
        db.session.add(medication_dose_unit)


def create_medication_frequencies():
    for k, v, in MEDICATION_FREQUENCIES:
        medication_frequency = MedicationFrequency(id=k, label=v)
        db.session.add(medication_frequency)

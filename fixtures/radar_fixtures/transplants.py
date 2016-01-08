from datetime import date
import random

from radar.models.organisations import Organisation
from radar.models.transplants import Transplant, TRANSPLANT_MODALITIES
from radar_fixtures.utils import random_date
from radar_fixtures.validation import validate_and_add


def create_transplants_f():
    organisations = Organisation.query.all()

    def create_transplants(patient, data_source, n):
        for _ in range(n):
            transplant = Transplant()
            transplant.patient = patient
            transplant.data_source = data_source
            transplant.date = random_date(patient.earliest_date_of_birth, date.today())
            transplant.modality = random.choice(TRANSPLANT_MODALITIES.keys())
            transplant.organisation = random.choice(organisations)

            if random.random() > 0.75:
                transplant.date_of_failure = random_date(transplant.date, date.today())

            validate_and_add(transplant)

    return create_transplants

import random
from datetime import date

from radar.models.dialysis import Dialysis, DIALYSIS_MODALITIES
from radar_fixtures.utils import random_date
from radar_fixtures.validation import validate_and_add


def create_dialysis_f():
    def create_dialysis(patient, data_source, n):
        for _ in range(n):
            dialysis = Dialysis()
            dialysis.patient = patient
            dialysis.data_source = data_source
            dialysis.from_date = random_date(patient.earliest_date_of_birth, date.today())

            if random.random() > 0.5:
                dialysis.to_date = random_date(dialysis.from_date, date.today())

            dialysis.modality = random.choice(DIALYSIS_MODALITIES.keys())

            validate_and_add(dialysis)

    return create_dialysis

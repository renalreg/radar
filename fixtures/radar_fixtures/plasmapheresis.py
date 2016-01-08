import random
from datetime import date

from radar.models.plasmapheresis import Plasmapheresis, PLASMAPHERESIS_NO_OF_EXCHANGES, PLASMAPHERESIS_RESPONSES
from radar_fixtures.utils import random_date
from radar_fixtures.validation import validate_and_add


def create_plasmapheresis_f():
    def create_plasmapheresis(patient, data_source, n):
        for _ in range(n):
            plasmapheresis = Plasmapheresis()
            plasmapheresis.patient = patient
            plasmapheresis.data_source = data_source
            plasmapheresis.from_date = random_date(patient.earliest_date_of_birth, date.today())

            if random.random() > 0.5:
                plasmapheresis.to_date = random_date(plasmapheresis.from_date, date.today())

            plasmapheresis.no_of_exchanges = random.choice(PLASMAPHERESIS_NO_OF_EXCHANGES.keys())
            plasmapheresis.response = random.choice(PLASMAPHERESIS_RESPONSES.keys())

            validate_and_add(plasmapheresis)

    return create_plasmapheresis

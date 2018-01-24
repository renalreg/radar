from datetime import date
import random

from radar.fixtures.utils import add, random_date
from radar.models.plasmapheresis import Plasmapheresis, PLASMAPHERESIS_NO_OF_EXCHANGES, PLASMAPHERESIS_RESPONSES


def create_plasmapheresis_f():
    def create_plasmapheresis(patient, source_group, source_type, n):
        for _ in range(n):
            plasmapheresis = Plasmapheresis()
            plasmapheresis.patient = patient
            plasmapheresis.source_group = source_group
            plasmapheresis.source_type = source_type
            plasmapheresis.from_date = random_date(patient.earliest_date_of_birth, date.today())

            if random.random() > 0.5:
                plasmapheresis.to_date = random_date(plasmapheresis.from_date, date.today())

            plasmapheresis.no_of_exchanges = random.choice(list(PLASMAPHERESIS_NO_OF_EXCHANGES.keys()))
            plasmapheresis.response = random.choice(list(PLASMAPHERESIS_RESPONSES.keys()))

            add(plasmapheresis)

    return create_plasmapheresis

from datetime import date
import random

from radar.fixtures.utils import random_date, add
from radar.models.results import Result, Observation, OBSERVATION_VALUE_TYPE


def create_results_f():
    observations = Observation.query.filter(Observation.value_type == OBSERVATION_VALUE_TYPE.REAL).all()

    def create_results(patient, source_group, source_type, x, y):
        for observation in random.sample(observations, min(x, len(observations))):
            min_value = observation.min_value

            if min_value is None:
                min_value = 0
            else:
                min_value = float(min_value)

            max_value = observation.max_value

            if max_value is None:
                max_value = 100
            else:
                max_value = float(max_value)

            for _ in range(y):
                result = Result()
                result.patient = patient
                result.source_group = source_group
                result.source_type = source_type
                result.observation = observation
                result.date = random_date(patient.earliest_date_of_birth, date.today())
                result.value = '%.2f' % random.uniform(min_value, max_value)
                add(result)

    return create_results

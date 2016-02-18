import random
from datetime import date

from radar.models.results import Result, Observation, OBSERVATION_VALUE_TYPE
from radar_fixtures.utils import random_date
from radar_fixtures.validation import validate_and_add


def create_results_f():
    observations = Observation.query.filter(Observation.value_type == OBSERVATION_VALUE_TYPE.REAL).all()

    def create_results(patient, source_group, source_type, x, y):
        for observation in random.sample(observations, min(x, len(observations))):
            min_value = observation.properties.get('min_value', 0)
            max_value = observation.properties.get('max_value', 100)

            for _ in range(y):
                result = Result()
                result.patient = patient
                result.source_group = source_group
                result.source_type = source_type
                result.observation = observation
                result.date = random_date(patient.earliest_date_of_birth, date.today())
                result.value = '%.2f' % random.uniform(min_value, max_value)
                validate_and_add(result)

    return create_results

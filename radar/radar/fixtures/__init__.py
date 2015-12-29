from radar.fixtures.comorbidities import create_disorders
from radar.fixtures.data_sources import create_data_sources
from radar.fixtures.diagnoses import create_cohort_diagnoses
from radar.fixtures.cohorts import create_cohorts
from radar.fixtures.results import create_result_specs, create_result_group_specs
from radar.fixtures.organisations import create_organisations
from radar.fixtures.users import create_users, DEFAULT_PASSWORD


def create_initial_data(password=DEFAULT_PASSWORD):
    create_users(password)

    create_organisations()
    create_data_sources()

    create_result_specs()
    create_result_group_specs()

    create_cohorts()
    create_cohort_diagnoses()

    create_disorders()

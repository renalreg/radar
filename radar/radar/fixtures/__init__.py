from radar.fixtures.comorbidities import create_disorders
from radar.fixtures.data_sources import create_data_sources
from radar.fixtures.diagnoses import create_cohort_diagnoses
from radar.fixtures.dialysis import create_dialysis_types
from radar.fixtures.cohorts import create_cohorts
from radar.fixtures.results import create_result_specs, create_result_group_specs
from radar.fixtures.patients import create_ethnicity_codes
from radar.fixtures.organisations import create_organisations


def create_initial_data():
    create_organisations()
    create_data_sources()

    create_result_specs()
    create_result_group_specs()

    create_cohorts()
    create_cohort_diagnoses()

    create_ethnicity_codes()
    create_dialysis_types()
    create_disorders()

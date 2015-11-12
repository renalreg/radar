from radar.data.comorbidities import create_disorders
from radar.data.data_sources import create_data_sources
from radar.data.diagnoses import create_cohort_diagnoses
from radar.data.dialysis import create_dialysis_types
from radar.data.cohorts import create_cohorts
from radar.data.results import create_result_specs, create_result_group_specs
from radar.data.patients import create_ethnicity_codes
from radar.data.organisations import create_organisations


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

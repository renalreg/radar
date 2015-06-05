from radar.lib.data.facilities import create_radar_facility
from radar.lib.data.dialysis import create_dialysis_types
from radar.lib.data.disease_groups import create_disease_groups
from radar.lib.data.lab_results import create_lab_group_definitions
from radar.lib.data.medications import create_medication_routes, create_medication_dose_units, \
    create_medication_frequencies
from radar.lib.data.patients import create_ethnicity_codes
from radar.lib.data.transplants import create_transplant_types
from radar.lib.data.units import create_units


def create_initial_data():
    create_radar_facility()

    create_lab_group_definitions()

    create_units()
    create_disease_groups()

    create_ethnicity_codes()

    create_transplant_types()

    create_dialysis_types()

    create_medication_routes()
    create_medication_dose_units()
    create_medication_frequencies()

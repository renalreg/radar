from radar.lib.data.dialysis import create_dialysis_types
from radar.lib.data.medications import create_medication_routes, create_medication_dose_units, \
    create_medication_frequencies
from radar.lib.data.patients import create_ethnicity_codes
from radar.lib.data.transplants import create_transplant_types


def create_initial_data():
    create_ethnicity_codes()
    create_transplant_types()
    create_dialysis_types()
    create_medication_routes()
    create_medication_dose_units()
    create_medication_frequencies()

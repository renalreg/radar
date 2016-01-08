from datetime import date

from radar.models.hospitalisations import Hospitalisation
from radar_fixtures.utils import random_date
from radar_fixtures.validation import validate_and_add


def create_hospitalisations_f():
    def create_hospitalisations(patient, data_source, n):
        for _ in range(n):
            hospitalisation = Hospitalisation()
            hospitalisation.patient = patient
            hospitalisation.data_source = data_source
            hospitalisation.date_of_admission = random_date(patient.earliest_date_of_birth, date.today())
            hospitalisation.date_of_discharge = random_date(hospitalisation.date_of_admission, date.today())
            hospitalisation.reason_for_admission = 'Test'

            validate_and_add(hospitalisation)

    return create_hospitalisations

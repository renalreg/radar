from datetime import date

from radar.models.hospitalisations import Hospitalisation

from radar_fixtures.utils import random_date, add


def create_hospitalisations_f():
    def create_hospitalisations(patient, source_group, source_type, n):
        for _ in range(n):
            hospitalisation = Hospitalisation()
            hospitalisation.patient = patient
            hospitalisation.source_group = source_group
            hospitalisation.source_type = source_type
            hospitalisation.date_of_admission = random_date(patient.earliest_date_of_birth, date.today())
            hospitalisation.date_of_discharge = random_date(hospitalisation.date_of_admission, date.today())
            hospitalisation.reason_for_admission = 'Test'
            add(hospitalisation)

    return create_hospitalisations

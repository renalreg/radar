from datetime import date
import random

from radar.fixtures.utils import random_date, add
from radar.models.groups import Group, GROUP_TYPE
from radar.models.transplants import Transplant, TRANSPLANT_MODALITIES


def create_transplants_f():
    hospitals = Group.query.filter(Group.type == GROUP_TYPE.HOSPITAL).all()

    def create_transplants(patient, source_group, source_type, n):
        for _ in range(n):
            transplant = Transplant()
            transplant.patient = patient
            transplant.source_group = source_group
            transplant.source_type = source_type
            transplant.date = random_date(patient.earliest_date_of_birth, date.today())
            transplant.modality = random.choice(TRANSPLANT_MODALITIES.keys())
            transplant.transplant_group = random.choice(hospitals)

            if random.random() > 0.75:
                transplant.date_of_failure = random_date(transplant.date, date.today())

            add(transplant)

    return create_transplants

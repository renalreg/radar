import random
from datetime import date

from radar.fixtures.utils import random_bool, random_date, add
from radar.models.renal_imaging import RenalImaging, RENAL_IMAGING_TYPES, RENAL_IMAGING_KIDNEY_TYPES


def create_renal_imaging_f():
    def create_renal_imaging(patient, source_group, source_type, n):
        for _ in range(n):
            renal_imaging = RenalImaging()
            renal_imaging.patient = patient
            renal_imaging.source_group = source_group
            renal_imaging.source_type = source_type
            renal_imaging.date = random_date(patient.earliest_date_of_birth, date.today())
            renal_imaging.imaging_type = random.choice(RENAL_IMAGING_TYPES.keys())
            renal_imaging.right_present = random_bool()
            renal_imaging.left_present = random_bool()

            if renal_imaging.right_present:
                renal_imaging.right_type = random.choice(RENAL_IMAGING_KIDNEY_TYPES.keys())
                renal_imaging.right_length = random.randint(11, 14)
                renal_imaging.right_cysts = random_bool()
                renal_imaging.right_stones = random_bool()
                renal_imaging.right_calcification = random_bool()

                if renal_imaging.right_calcification:
                    renal_imaging.right_nephrocalcinosis = random_bool()
                    renal_imaging.right_nephrolithiasis = random_bool()

            if renal_imaging.left_present:
                renal_imaging.left_type = random.choice(RENAL_IMAGING_KIDNEY_TYPES.keys())
                renal_imaging.left_length = random.randint(11, 14)
                renal_imaging.left_cysts = random_bool()
                renal_imaging.left_stones = random_bool()
                renal_imaging.left_calcification = random_bool()

                if renal_imaging.left_calcification:
                    renal_imaging.left_nephrocalcinosis = random_bool()
                    renal_imaging.left_nephrolithiasis = random_bool()

            add(renal_imaging)

    return create_renal_imaging

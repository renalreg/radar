from radar.concepts.core import Concept
from radar.sda.models import SDAEncounter
from radar.lib.validators import required


class HospitalisationConcept(Concept):
    validators = {
        'date_of_admission': [required],
    }

    def __init__(self, date_of_admission, date_of_discharge):
        super(HospitalisationConcept, self).__init__()

        self.date_of_admission = date_of_admission
        self.date_of_discharge = date_of_discharge

    def validate(self):
        if not super(HospitalisationConcept, self).validate():
            return False

        if self.date_of_discharge is not None and self.date_of_discharge < self.date_of_admission:
            self.errors['date_of_discharge'].append('Must be on or after date of admission.')

        return not self.errors

    def to_sda(self, sda_bundle):
        sda_encounter = SDAEncounter()

        data = {
            'from_date': self.date_of_admission,
        }

        if self.date_of_discharge is not None:
            data['to_date'] = self.date_of_discharge

        sda_encounter.data = data
        sda_bundle.sda_encounters.append(sda_encounter)
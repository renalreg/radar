from radar.concepts.core import Concept
from radar.sda.models import SDAEncounter
from radar.validators import required


class DialysisConcept(Concept):
    validators = {
        'from_date': [required],
        'dialysis_type': [required],
    }

    def __init__(self, from_date, to_date, dialysis_type):
        super(DialysisConcept, self).__init__()

        self.from_date = from_date
        self.to_date = to_date
        self.dialysis_type = dialysis_type

    def validate(self):
        if not super(DialysisConcept, self).validate():
            return False

        if self.to_date is not None and self.to_date < self.from_date:
            self.errors['to_date'].append('Must be on or after from date.')

        return not self.errors

    def to_sda(self, sda_bundle):
        sda_encounter = SDAEncounter()

        data = {
            'from_time': self.from_date,
            'admit_reason': {
                'sda_coding_standard': 'RADAR',
                'code': self.dialysis_type.id,
                'description': self.dialysis_type.name,
            },
            'publicity_code': {
                'sda_coding_standard': 'RADAR',
                'code': self.dialysis_type.id,
                'description': self.dialysis_type.name,
            }
        }

        if self.to_date is not None:
            data['to_time'] = self.to_date

        sda_encounter.data = data

        sda_bundle.sda_encounters.append(sda_encounter)
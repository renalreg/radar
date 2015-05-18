from radar.concepts.core import Concept
from radar.validators import required, not_empty


class DialysisConcept(Concept):
    validators = {
        'from_date': [required],
        'to_date': [not_empty],
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
        pass
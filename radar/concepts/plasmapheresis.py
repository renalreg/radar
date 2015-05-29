from radar.concepts.core import Concept
from radar.sda.models import SDAProcedure
from radar.lib.validators import required


class PlasmapheresisConcept(Concept):
    validators = {
        'from_date': [required],
        'no_of_exchanges': [required],
        'response': [required],
    }

    def __init__(self, from_date, to_date, no_of_exchanges, response):
        super(PlasmapheresisConcept, self).__init__()

        self.from_date = from_date
        self.to_date = to_date
        self.no_of_exchanges = no_of_exchanges
        self.response = response

    def validate(self):
        if not super(PlasmapheresisConcept, self).validate():
            return False

        if self.to_date is not None and self.to_date < self.from_date:
            self.errors['to_date'].append('Must be on or after from date.')

        return not self.errors

    def to_sda(self, sda_bundle):
        sda_procedure = SDAProcedure()

        data = {
            'from_time': self.from_date,
            'procedure': {
                'sda_coding_standard': 'RADAR',
                'code': 'PLASMAPHERESIS',  # TODO
                'description': 'Plasmapheresis',
            },
        }

        if self.to_date is not None:
            data['to_time'] = self.to_date

        sda_procedure.data = data
        sda_bundle.sda_procedures.append(sda_procedure)
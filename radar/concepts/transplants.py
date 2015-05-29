from radar.concepts.core import Concept
from radar.sda.models import SDAProcedure
from radar.lib.validators import required


class TransplantConcept(Concept):
    validators = {
        'transplant_date': [required],
        'transplant_type': [required],
    }

    def __init__(self, transplant_date, transplant_type):
        super(TransplantConcept, self).__init__()

        self.transplant_date = transplant_date
        self.transplant_type = transplant_type

    def to_sda(self, sda_bundle):
        sda_procedure = SDAProcedure()

        data = {
            'procedure_time': self.transplant_date,
            'procedure': {
                'sda_coding_standard': 'RADAR',
                'code': self.transplant_type.id,
                'description': self.transplant_type.id,
            }
        }

        sda_procedure.data = data

        sda_bundle.sda_procedures.append(sda_procedure)
from collections import defaultdict
from radar.concepts.dialysis import DialysisConcept


class DialysisToDialysisConcept(object):
    def __init__(self, dialysis):
        self.dialysis = dialysis

        self.dialysis_concept = DialysisConcept(
            dialysis.from_date,
            dialysis.to_date,
            dialysis.dialysis_type
        )

    def validate(self):
        valid = True
        errors = defaultdict(list)

        if not self.dialysis_concept.validate():
            valid = False
            errors['from_date'].extend(self.dialysis_concept.errors['from_date'])
            errors['to_date'].extend(self.dialysis_concept.errors['to_date'])
            errors['dialysis_type_id'].extend(self.dialysis_concept.errors['dialysis_type'])

        return valid, errors

    def to_sda(self, sda_bundle):
        self.dialysis_concept.to_sda(sda_bundle)
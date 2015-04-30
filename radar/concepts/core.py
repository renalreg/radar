from collections import defaultdict
from radar.models import Facility
from radar.sda.models import SDAMedication, SDABundle
from radar.validators import ValidationError, StopValidation, required, not_empty


class Concept(object):
    validators = {}

    def __init__(self):
        self.errors = defaultdict(list)

    def validate(self):
        self.errors = defaultdict(list)

        for model_key, validators in self.validators.items():
            model_value = getattr(self, model_key)

            for validator in validators:
                try:
                    validator(model_value)
                except ValidationError as e:
                    self.errors[model_key].append(e.message)
                    break
                except StopValidation:
                    break

        return not self.errors

    def to_sda(self):
        pass

def validate_concepts(concepts):
    valid = False
    errors = defaultdict(list)

    for concept in concepts:
        valid, errors = concept.validate()

        if not valid:
            valid = False

            for field, field_errors in errors:
                errors[field].extend(field_errors)

    return valid, errors

def concepts_to_sda_bundle(patient, concepts):
    facility = Facility.query.get(1)

    sda_bundle = SDABundle(patient=patient, facility=facility)

    for concept in concepts:
        concept.to_sda(sda_bundle)

    return sda_bundle
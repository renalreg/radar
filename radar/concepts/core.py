from collections import defaultdict

from radar.models.base import Facility
from radar.sda.models import SDABundle
from radar.validators import ValidationError, StopValidation


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
    valid = True
    errors = defaultdict(list)

    for concept in concepts:
        valid, concept_errors = concept.validate()

        if not valid:
            valid = False

            for field, field_errors in concept_errors.items():
                errors[field].extend(field_errors)

    return valid, errors


def concepts_to_sda_bundle(concepts, patient):
    # TODO
    facility = Facility.query.get(1)

    sda_bundle = SDABundle(patient=patient, facility=facility)

    for concept in concepts:
        concept.to_sda(sda_bundle)

    return sda_bundle
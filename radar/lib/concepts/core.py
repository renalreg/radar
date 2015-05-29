from collections import defaultdict

from radar.lib.validators import ValidationError, StopValidation


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